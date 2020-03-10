# -*- coding: utf-8 -*-

from django.db import models


class Timestamps(models.Model):
    """Usefull timestamps fields mixin."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        """String representation."""
        return "created_at: {0}, updated_at: {1}".format(
            self.created_at, self.updated_at,
        )
