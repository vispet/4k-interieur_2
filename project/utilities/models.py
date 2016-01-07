"""
Models
"""

from django.db import models

from feincms.models import Base

from .validators import validate_slug_lower


class ArticleBase(Base):
    """
    An abstract article base
    """
    slug = models.SlugField(unique=True, validators=[validate_slug_lower])
    title = models.CharField(max_length=255)
    teaser = models.TextField()
    image = models.ImageField(upload_to="article/teasers", width_field="width",
                              height_field="height")
    width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    height = models.PositiveIntegerField(null=True, blank=True, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        """
        Options
        """
        abstract = True

    def __unicode__(self):
        """
        Unicode repr
        """
        return self.title
