# core/modules/github_client.py
import requests
from core.config import config
from core.modules.cache_manager import CacheManager

class GitHubClient:
    """Cliente HTTP desacoplado para la API de GitHub con soporte de caché y análisis multi-nivel de lenguajes."""

    def __init__(self):
        self.token = config.GH_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "Core-Secure-GitHub-Engine"
        })

    def _fetch_raw_languages(self) -> tuple[dict, int, str]:
        """Obtiene y cachea la data cruda de repositorios y bytes por lenguaje desde la API."""
        cache_key = "github_raw_languages_payload"
        cached = CacheManager.get(cache_key)
        if cached:
            return cached

        user_res = self.session.get("https://api.github.com/user", timeout=10)
        username = user_res.json().get("login", "GitHub") if user_res.status_code == 200 else "GitHub"

        repos = []
        page = 1
        per_page = 100

        while True:
            url = f"https://api.github.com/user/repos?visibility=all&affiliations=owner,collaborator,organization_member&per_page={per_page}&page={page}"
            res = self.session.get(url, timeout=10)
            if res.status_code != 200:
                break
            data = res.json()
            if not data or not isinstance(data, list):
                break
            repos.extend(data)
            if len(data) < per_page:
                break
            page += 1

        global_languages = {}
        total_bytes = 0

        for repo in repos:
            lang_url = repo.get("languages_url")
            if not lang_url:
                continue
            lang_res = self.session.get(lang_url, timeout=5)
            if lang_res.status_code == 200:
                for lang, bytes_count in lang_res.json().items():
                    global_languages[lang] = global_languages.get(lang, 0) + bytes_count
                    total_bytes += bytes_count

        payload = (global_languages, total_bytes, username)
        CacheManager.set(cache_key, payload, ttl_seconds=21600)
        return payload

    def all_languages(self) -> tuple[list[tuple[str, int, float]], int, str]:
        """Retorna todos los lenguajes detectados, sus bytes y porcentajes exactos (incluyendo 0%)."""
        global_languages, total_bytes, username = self._fetch_raw_languages()
        result = []
        if total_bytes > 0:
            for lang, b_count in global_languages.items():
                pct = (b_count / total_bytes) * 100.0
                result.append((lang, b_count, pct))

        return sorted(result, key=lambda x: x[1], reverse=True), total_bytes, username

    def top_languages(self, min_percentage: float = 1.0) -> tuple[list[tuple[str, int, float]], int, str]:
        """Retorna el top filtrado de lenguajes que superan el umbral porcentual especificado."""
        langs, total_bytes, username = self.all_languages()
        filtered = [(lang, b, pct) for lang, b, pct in langs if pct >= min_percentage]
        return filtered, total_bytes, username