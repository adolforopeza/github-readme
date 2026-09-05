# core/modules/github_client.py
import requests
from core.config import config
from core.modules.cache_manager import CacheManager

class GitHubClient:
    """Cliente HTTP optimizado que consume directamente el endpoint consolidado de lenguajes por repositorio o globales."""

    def __init__(self):
        self.token = config.GH_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "Core-Secure-GitHub-Engine"
        })

    def _fetch_languages_via_endpoint(self, public_only: bool) -> tuple[list[tuple[str, int, float]], int, str]:
        """Obtiene la lista de repositorios, extrae el link directo de lenguajes de cada uno y calcula los porcentajes con precisión."""
        cache_key = f"github_languages_endpoint_direct_public_{public_only}_v6"
        cached = CacheManager.get(cache_key)
        if cached:
            return cached

        user_res = self.session.get("https://api.github.com/user", timeout=10)
        username = user_res.json().get("login", "adolforopeza") if user_res.status_code == 200 else "adolforopeza"

        repos = []
        page = 1
        per_page = 100

        while True:
            url = f"https://api.github.com/user/repos?type=owner&per_page={per_page}&page={page}"
            res = self.session.get(url, timeout=10)
            if res.status_code != 200:
                break
            data = res.json()
            if not data or not isinstance(data, list):
                break

            data = [repo for repo in data if not repo.get("fork", False)]
            if public_only:
                data = [repo for repo in data if not repo.get("private", True)]

            repos.extend(data)
            if len(data) < per_page:
                break
            page += 1

        global_languages = {}
        total_bytes = 0

        for repo in repos:
            # Uso directo del endpoint de lenguajes por repositorio (ej: /repos/{owner}/{repo}/languages)
            lang_url = repo.get("languages_url")
            if not lang_url:
                continue

            lang_res = self.session.get(lang_url, timeout=5)
            if lang_res.status_code == 200:
                lang_data = lang_res.json()
                if isinstance(lang_data, dict):
                    for lang, bytes_count in lang_data.items():
                        if bytes_count > 0:
                            global_languages[lang] = global_languages.get(lang, 0) + bytes_count
                            total_bytes += bytes_count

        result = []
        if total_bytes > 0:
            for lang, b_count in global_languages.items():
                pct = round((b_count / total_bytes) * 100.0, 2)
                result.append((lang, b_count, pct))

        sorted_result = sorted(result, key=lambda x: x[1], reverse=True)
        payload = (sorted_result, total_bytes, username)

        CacheManager.set(cache_key, payload, ttl_seconds=1)
        return payload

    def all_languages(self) -> tuple[list[tuple[str, int, float]], int, str]:
        """Retorna todos los lenguajes de la infraestructura global usando los endpoints individuales de repositorios."""
        return self._fetch_languages_via_endpoint(public_only=False)

    def top_languages(self, min_percentage: float = 0.0) -> tuple[list[tuple[str, int, float]], int, str]:
        """Retorna el top de lenguajes calculado exclusivamente sobre repositorios públicos mediante sus endpoints dedicados."""
        return self._fetch_languages_via_endpoint(public_only=True)