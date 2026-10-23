# core/modules/project.py
from core.constants.projects import PROJECTS

class Projects:
    """Responsable exclusivo del procesamiento y formateo de catálogos de proyectos externos."""

    @staticmethod
    def get_project_markdown(project_name) -> str:
        """Genera el marcado Markdown optimizado para inserción directa en el README a partir de las constantes."""
        buffer = []
        projects = PROJECTS.get(project_name, [])
        for proj in projects:
            buffer.append(f"### [{proj['title']}]({proj['url']})")
            buffer.append(f"{proj['short_description']}\n")
        return "\n".join(buffer)
    @staticmethod
    def get_profile_markdown() -> str:
        """Genera el marcado Markdown optimizado para la sección de perfil profesional en el README."""
        profile = PROJECTS.get("PROFILE", {})
        title = profile.get("title", "")
        description = profile.get("description", "")

        buffer = []
        if title:
            buffer.append(f"## {title}\n")
        if description:
            buffer.append(f"{description}\n")

        return "\n".join(buffer)