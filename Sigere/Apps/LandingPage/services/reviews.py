from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from django.db.models import Avg, Count

from ..models import Reserva, Resena, EspacioDeportivo


@dataclass
class ReviewStats:
    promedio: float
    total: int


def get_pending_reservations_for_review(usuario) -> Iterable[Reserva]:
    """Reservas pasadas sin reseña disponible para el usuario."""
    return (
        Reserva.objects
        .for_user(usuario)
        .past()
        .filter(cancelada=False, resena__isnull=True)
        .order_by('-fecha')
    )


def get_review_stats_for_space(espacio: EspacioDeportivo) -> ReviewStats:
    resumen = espacio.resenas.aggregate(promedio=Avg('calificacion'), total=Count('id'))
    return ReviewStats(promedio=float(resumen['promedio'] or 0), total=resumen['total'] or 0)


def get_top_rated_spaces(limit: int = 5):
    return (
        EspacioDeportivo.objects
        .filter(total_resenas__gt=0)
        .order_by('-calificacion_promedio', '-total_resenas')[:limit]
    )


__all__ = [
    'ReviewStats',
    'get_pending_reservations_for_review',
    'get_review_stats_for_space',
    'get_top_rated_spaces',
]
