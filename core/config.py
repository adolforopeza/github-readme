# core/config.py
import os
from typing import Optional

class SecureConfig:
    """Valida y encapsula de manera segura las variables de entorno críticas."""

    @staticmethod
    def _get_env(key: str, default: Optional[str] = None, required: bool = False) -> str:
        value = os.getenv(key, default)
        if required and not value:
            raise RuntimeError(f"Fallo de seguridad: Variable de entorno obligatoria no encontrada -> {key}")
        return value or ""

    @property
    def GH_TOKEN(self) -> str:
        return self._get_env("GH_TOKEN", required=True)

    @property
    def VERC_COMMIT(self) -> str:
        return self._get_env("VERCEL_GIT_COMMIT_SHA", "local-dev")

config = SecureConfig()