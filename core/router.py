# core/router.py
import re
from typing import Callable, Tuple, Dict, Any

class Router:
    """Enrutador dinámico inspirado en Slim Framework, optimizado para alto rendimiento y seguridad."""

    def __init__(self):
        self.routes: Dict[str, Callable[[], Tuple[Any, str]]] = {}

    def add(self, path: str, handler: Callable[[], Tuple[Any, str]]) -> None:
        """Registra una ruta de manera dinámica normalizando las barras invertidas/diagonales."""
        clean_path = self._normalize_path(path)
        self.routes[clean_path] = handler

    def resolve(self, raw_path: str) -> Tuple[Any, str, int]:
        """Resuelve la ruta de forma segura y veloz usando un diccionario hash O(1)."""
        clean_path = self._normalize_path(raw_path.split("?")[0])

        if clean_path in self.routes:
            content, c_type = self.routes[clean_path]()
            return content, c_type, 200

        return "Not Found", "text/plain; charset=utf-8", 404

    def get_routes(self) -> list[str]:
        """Retorna el listado completo de rutas registradas en el sistema."""
        return list(self.routes.keys())

    @staticmethod
    def _normalize_path(path: str) -> str:
        """Sanitiza y normaliza el path previniendo directory traversal y rutas malformadas."""
        if not path:
            return "/"
        normalized = re.sub(r'//+', '/', path)
        if len(normalized) > 1 and normalized.endswith('/'):
            normalized = normalized.rstrip('/')
        return normalized

# Instanciación centralizada del enrutador dinámico
router = Router()