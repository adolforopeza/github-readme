# core/routes/profile.py
from core.modules.project import Projects

def handle_profile() -> tuple[str, str]:
    """Controlador que expone el listado general de proyectos de la infraestructura[cite: 5]."""
    markdown_content = Projects.get_profile_markdown()
    return markdown_content, "text/markdown; charset=utf-8"