from __future__ import annotations

from django import template

register = template.Library()


@register.simple_tag
def star_range(calificacion: float, max_stars: int = 5):
    """Devuelve la lista de estrellas completas, medias y vacías."""
    calificacion = calificacion or 0
    full_stars = int(calificacion)
    half_star = 1 if (calificacion - full_stars) >= 0.5 else 0
    empty_stars = max(0, max_stars - full_stars - half_star)
    return {
        'full': range(full_stars),
        'half': range(half_star),
        'empty': range(empty_stars),
    }
