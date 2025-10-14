from __future__ import annotations

from django.db import models
from django.utils import timezone


class ReservaQuerySet(models.QuerySet):
    """QuerySet especializado con operaciones reutilizables sobre reservas."""

    def for_user(self, user):
        return self.filter(usuario=user)

    def active(self):
        today = timezone.now().date()
        return self.filter(fecha__gte=today, cancelada=False)

    def past(self):
        today = timezone.now().date()
        return self.filter(fecha__lt=today)

    def cancelled(self):
        return self.filter(cancelada=True)

    def ordered_recent_first(self):
        return self.order_by('-fecha', '-hora')


ReservaManager = ReservaQuerySet.as_manager()


class ReviewQuerySet(models.QuerySet):
    """Consultas reutilizables para reseñas de espacios deportivos."""

    def for_space(self, espacio):
        return self.filter(espacio=espacio)

    def for_user(self, usuario):
        return self.filter(usuario=usuario)

    def published(self):
        return self.filter(publicada=True)

    def ordered_recent_first(self):
        return self.order_by('-created_at')
