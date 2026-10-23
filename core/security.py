# core/security.py
import html

class SecurityUtils:
    """Implementa defensas contra inyecciones y sanitización de datos para SVGs y texto."""

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Escapa caracteres especiales para prevenir XSS e inyección de código en SVGs o HTML."""
        if not isinstance(text, str):
            return str(text)
        return html.escape(text, quote=True)