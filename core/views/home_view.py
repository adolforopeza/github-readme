# core/views/home_view.py
import os
from core.constants.projects import PROJECTS
from core.modules.template_engine import TemplateEngine

def get_home_html(links_html: str) -> str:
    """Renderiza la vista principal utilizando el motor de plantillas y componentes modulares."""
    profile = PROJECTS.get("PROFILE", {})
    name = profile.get("name", "")
    company = profile.get("company", "")
    title = profile.get("title", "")
    description = profile.get("description", "")
    tech_stack = profile.get("tech_stack", [])

    tech_tags_html = "".join([f'<span class="tag">{tech}</span>' for tech in tech_stack])

    # Leer el contenido del CSS para inyectarlo en base.html si se requiere o mantener la ruta estática
    css_path = TemplateEngine._get_abs_path("static/css/style.css")
    css_content = TemplateEngine._load_file_cached(css_path) if os.path.exists(css_path) else ""

    context = {
        "title": f"{name} - {title}",
        "name": name,
        "company": company,
        "role": title,
        "description": description,
        "tech_tags_html": tech_tags_html,
        "endpoints": f"<h3>Endpoints Dinámicos Disponibles:</h3>\n<ul>\n{links_html}\n</ul>",
        "css_content": css_content
    }

    components = {
        "header": "templates/components/header.html",
        "bio": "templates/components/bio.html",
        "tech_stack": "templates/components/tech_stack.html"
    }

    return TemplateEngine.render("base.html", context, components)