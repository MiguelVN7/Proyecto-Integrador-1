from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, Type

from django.conf import settings
from django.utils.module_loading import import_string

from .ai_provider import AIContentProvider, OpenAIContentProvider, AIProviderError
from .reviews import (
	ReviewStats,
	get_pending_reservations_for_review,
	get_review_stats_for_space,
	get_top_rated_spaces,
)


def _resolve_provider_class(config: Dict[str, Any]) -> Type[AIContentProvider]:
	class_path = config.get("CLASS")
	if not class_path:
		return OpenAIContentProvider
	provider_cls = import_string(class_path)
	if not issubclass(provider_cls, AIContentProvider):
		raise AIProviderError(
			f"La clase configurada '{class_path}' no implementa AIContentProvider."
		)
	return provider_cls


@lru_cache(maxsize=1)
def get_ai_provider() -> AIContentProvider:
	"""Obtiene una instancia del proveedor de contenido IA configurado."""

	config = getattr(settings, "AI_CONTENT_PROVIDER", {})
	provider_cls = _resolve_provider_class(config)

	options = dict(config.get("OPTIONS", {}))
	options.setdefault("api_key", getattr(settings, "OPENAI_API_KEY", None))

	return provider_cls(**options)


__all__ = [
	"AIProviderError",
	"AIContentProvider",
	"OpenAIContentProvider",
	"get_ai_provider",
	"ReviewStats",
	"get_pending_reservations_for_review",
	"get_review_stats_for_space",
	"get_top_rated_spaces",
]
