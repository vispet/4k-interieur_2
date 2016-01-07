"""
Models
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from utilities import content_types
from utilities.models import ArticleBase


class NewsItem(ArticleBase):
    """
    A news item object
    """
    published = models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True, blank=True)

    class Meta(object):
        """
        Options
        """
        get_latest_by = "published_on"
        ordering = ("-published_on",)

    def save(self, *args, **kwargs):
        """
        add published_on date when model is published
        """
        if self.published and not self.published_on:
            self.published_on = timezone.now()
        super(NewsItem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Get url
        """
        if not self.published:
            return None
        return reverse("news:item", kwargs={
            "slug": self.slug,
        })


NewsItem.register_regions(
    ("content", _("Content")),
    ("gallery", _("Gallery")),
)
NewsItem.create_content_type(content_types.MarkdownContent,
                             regions=("content",))
NewsItem.create_content_type(content_types.CaptionedImageContent,
                             regions=("content",))
NewsItem.create_content_type(content_types.ImageContent,
                             regions=("gallery",))
