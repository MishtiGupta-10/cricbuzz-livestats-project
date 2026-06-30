from __future__ import annotations

from functools import wraps
from time import monotonic
from typing import Any, Callable, TypeVar

from backend.core.config import settings

T = TypeVar("T")

_cache_store: dict[tuple[str, tuple[Any, ...], tuple[tuple[str, Any], ...]], tuple[float, Any]] = {}


def ttl_cache(ttl_seconds: int | None = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    ttl = ttl_seconds or settings.cache_ttl_seconds

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            now = monotonic()
            cached = _cache_store.get(key)

            if cached:
                expires_at, value = cached
                if now < expires_at:
                    return value

            value = func(*args, **kwargs)
            _cache_store[key] = (now + ttl, value)
            return value

        return wrapper

    return decorator


def clear_cache() -> None:
    _cache_store.clear()
