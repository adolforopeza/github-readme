# core/routes/home.py
from core.views.home_view import get_home_html
from core.router import router

def handle_home() -> tuple[str, str]:
    """Controlador para la ruta principal del dashboard."""
    links_html = "".join([f'<li><a href="{r}"><span class="path-name">{r}</span><span class="path-action">Access &rarr;</span></a></li>' for r in router.get_routes()])
    return get_home_html(links_html), "text/html; charset=utf-8"