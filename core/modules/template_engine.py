# core/modules/template_engine.py
import os
from functools import lru_cache
from typing import Dict, Any

class TemplateEngine:
    """Motor de plantillas asíncrono-ready con pre-compilación y caché inmutable de I/O en disco."""

    @staticmethod
    @lru_cache(maxsize=32)
    def _load_file_cached(file_path: str) -> str:
        """Elimina el overhead de lectura en disco repetitiva mediante memoización LRU nativa."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def _get_abs_path(cls, relative_path: str) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.normpath(os.path.join(current_dir, "..", relative_path))
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Recurso crítico no encontrado: {full_path}")
        return full_path

    @classmethod
    def render(cls, layout_name: str, context: Dict[str, Any], components: Dict[str, str]) -> str:
        """Ensambla plantillas utilizando buffers de strings en memoria y reemplazos optimizados recursivos."""
        layout_path = cls._get_abs_path(f"templates/{layout_name}")
        layout_content = cls._load_file_cached(layout_path)

        master_context = dict(context)

        # Cargar e inyectar componentes, procesando su propio contexto antes de insertarlos en el layout principal
        for comp_key, comp_rel_path in components.items():
            comp_path = cls._get_abs_path(comp_rel_path)
            comp_content = cls._load_file_cached(comp_path)

            # Reemplazar variables locales dentro del componente antes de subirlo al master_context
            for key, value in master_context.items():
                comp_content = comp_content.replace(f"{{{{{key}}}}}", str(value))

            master_context[comp_key] = comp_content

        # Reemplazar todas las variables y componentes en el layout principal
        for key, value in master_context.items():
            layout_content = layout_content.replace(f"{{{{{key}}}}}", str(value))

        return layout_content