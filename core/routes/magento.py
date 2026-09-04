# core/routes/magento.py
from core.modules.project import Projects

def handle_magento() -> tuple[str, str]:
    """Controlador que expone la lista de proyectos Magento formateados para Markdown usando el formateador independiente."""
    markdown_content = Projects.get_project_markdown("MAGENTO")
    return markdown_content, "text/markdown; charset=utf-8"