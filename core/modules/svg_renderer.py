# core/modules/svg_renderer.py
import math
from core.security import SecurityUtils
from core.constants.colors import LANG_COLORS

class SVGRenderer:
    """Responsable exclusivo de la síntesis geométrica y rasterización vectorial de assets SVG planos."""

    @staticmethod
    def render_languages_svg(langs_data: list, total_bytes: int, username: str, title: str = None) -> str:
        """Renderiza el SVG con estilo flat y soporte para título dinámico inyectado por parámetro."""
        safe_user = SecurityUtils.sanitize_text(username)

        # Resolución del título dinámico con respaldo por defecto
        raw_title = title if title is not None else f"{safe_user}'s Core Languages (>1%)"
        safe_title = SecurityUtils.sanitize_text(raw_title)

        normalized_langs = []
        for item in langs_data:
            if len(item) == 3:
                lang, bytes_count, _ = item
            else:
                lang, bytes_count = item
            normalized_langs.append((lang, bytes_count))

        num_langs = len(normalized_langs)
        rows = math.ceil(num_langs / 3) if num_langs > 0 else 1
        svg_height = max(120, 50 + (rows * 25) + 15)

        svg = f'''<svg width="490" height="{svg_height}" viewBox="0 0 490 {svg_height}" xmlns="http://www.w3.org/2000/svg">
            <style>
                .title {{ font-family: -apple-system, sans-serif; font-size: 14px; font-weight: 600; fill: #c9d1d9; }}
                .lang-text {{ font-family: -apple-system, sans-serif; font-size: 12px; fill: #8b949e; }}
            </style>
            <rect width="490" height="{svg_height}" fill="#0d1117"/>
            <text x="20" y="30" class="title">{safe_title}</text>
        '''

        for i, (lang, bytes_count) in enumerate(normalized_langs):
            pct = (bytes_count / total_bytes) * 100 if total_bytes > 0 else 0.0
            color = LANG_COLORS.get(lang, "777BB4")
            safe_lang = SecurityUtils.sanitize_text(lang)
            col = i % 3
            row = i // 3
            cx = 20 + (col * 155)
            cy = 60 + (row * 25)

            svg += f'''
                <circle cx="{cx + 5}" cy="{cy}" r="5" fill="#{color}"/>
                <text x="{cx + 18}" y="{cy + 4}" class="lang-text">{safe_lang}: {pct:.1f}%</text>
            '''

        svg += '</svg>'
        return svg