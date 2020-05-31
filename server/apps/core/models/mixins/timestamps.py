# -*- coding: utf-8 -*-

from django.db import models


class Timestamps(models.Model):
    """Usefull timestamps fields mixin."""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)  # noqa: DJ12
    updated_at = models.DateTimeField(auto_now=True)  # noqa: DJ12

    def __str__(self):
        """String representation."""
        return "created_at: {0}, updated_at: {1}".format(
            self.created_at, self.updated_at,
        )
