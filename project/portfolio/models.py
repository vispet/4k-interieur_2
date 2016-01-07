"""
Models
"""

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from adminsortable.models import SortableMixin

from utilities import content_types
from utilities.models import ArticleBase


class Project(ArticleBase, SortableMixin):
    """
    A portfolio project
    """
    active = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, editable=False,
                                        db_index=True)

    class Meta(object):
        """
        Options
        """
        ordering = ["order"]

    def get_absolute_url(self):
        """
        Get the reversed url
        """
        if not self.active:
            return None
        return reverse("portfolio:project", kwargs={
            "slug": self.slug,
        })

Project.register_regions(
    ("content", _("Content")),
    ("intro", _("Intro images")),
    ("gallery", _("Gallery"))
)
Project.create_content_type(content_types.MarkdownContent,
                            regions=("content",))
Project.create_content_type(content_types.CaptionedImageContent,
                            regions=("content",))
Project.create_content_type(content_types.ImageContent,
                            regions=("intro", "gallery"))
