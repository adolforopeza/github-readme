# core/routes/languages.py
from core.modules.github_client import GitHubClient
from core.modules.svg_renderer import SVGRenderer
from core.modules.cache_manager import CacheManager

def handle_top_languages() -> tuple[str, str]:
    """Controlador optimizado para generar el SVG del top de lenguajes filtrados (>1%)."""
    client = GitHubClient()
    sorted_langs, total_bytes, username = client.top_languages(min_percentage=1.0)

    cache_key = f"svg_top_languages_{username}"
    cached_svg = CacheManager.get(cache_key)

    if cached_svg:
        return cached_svg, "image/svg+xml; charset=utf-8"

    svg_content = SVGRenderer.render_languages_svg(
        sorted_langs, total_bytes, username, title=f"{username}'s Top Languages (>1%)"
    )
    CacheManager.set(cache_key, svg_content, ttl_seconds=86400)

    return svg_content, "image/svg+xml; charset=utf-8"

def handle_all_languages() -> tuple[str, str]:
    """Controlador optimizado para generar el SVG con todos los lenguajes detectados."""
    client = GitHubClient()
    sorted_langs, total_bytes, username = client.all_languages()

    cache_key = f"svg_all_languages_{username}"
    cached_svg = CacheManager.get(cache_key)

    if cached_svg:
        return cached_svg, "image/svg+xml; charset=utf-8"

    svg_content = SVGRenderer.render_languages_svg(
        sorted_langs, total_bytes, username, title=f"{username}'s All Languages"
    )
    CacheManager.set(cache_key, svg_content, ttl_seconds=86400)

    return svg_content, "image/svg+xml; charset=utf-8"