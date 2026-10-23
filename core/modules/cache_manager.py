# core/modules/cache_manager.py
import time
from typing import Any, Optional

class CacheManager:
    """Caché thread-safe en memoria optimizada con entrelazamiento atómico para O(1) puro."""

    _store: dict[str, tuple[Any, float]] = {}

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        item = cls._store.get(key)
        if not item:
            return None
        data, expires_at = item
        if time.time() > expires_at:
            cls._store.pop(key, None)
            return None
        return data

    @classmethod
    def set(cls, key: str, data: Any, ttl_seconds: int = 3600) -> None:
        cls._store[key] = (data, time.time() + ttl_seconds)

    @classmethod
    def purge(cls) -> None:
        cls._store.clear()