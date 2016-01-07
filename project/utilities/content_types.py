"""
Generic feincms content types for inclusion or extention in site
"""

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template.loader import render_to_string
from django.template import RequestContext


class ModelRenderMixin(object):
    """
    Renders a model based on template variable
    """

    template = None

    def render(self, request):
        """
        Render the content
        """
        if self.template is None:
            raise ImproperlyConfigured("No template!")

        return render_to_string(self.template, {
            "model": self,
        }, RequestContext(request))


class ImageContent(ModelRenderMixin, models.Model):
    """
    An in text image image
    """
    template = "content-types/image.html"
    image = models.ImageField(upload_to="ct/image", width_field="width",
                              height_field="height")
    width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    height = models.PositiveIntegerField(null=True, blank=True, editable=False)

    class Meta(object):
        """
        Options
        """
        abstract = True


class CaptionedImageContent(ImageContent):
    """
    Add cap
    """
    template = "content-types/caption-image.html"
    caption = models.TextField(null=True, blank=True)

    class Meta(object):
        """
        Options
        """
        abstract = True


class MarkdownContent(ModelRenderMixin, models.Model):
    """
    A markdown content type
    """
    template = "content-types/markdown.html"

    content = models.TextField()

    class Meta(object):
        """
        Options
        """
        abstract = True
