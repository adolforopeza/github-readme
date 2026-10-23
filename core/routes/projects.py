# core/routes/projects.py
from core.modules.project import Projects

def handle_projects() -> tuple[str, str]:
    """Controlador que expone el listado general de proyectos de la infraestructura[cite: 5]."""
    markdown_content = Projects.get_project_markdown("PHP")
    return markdown_content, "text/markdown; charset=utf-8"