"""
Models
"""

from django.db import models


class ManifestEntryModel(models.Model):
    """
    Canonical storage
    """
    name = models.CharField(unique=True, max_length=255)
    remote_name = models.CharField(null=True, blank=True, max_length=255)
    buffer_name = models.CharField(null=True, blank=True, max_length=255)
    remote_url = models.CharField(null=True, blank=True, max_length=255)
