"""
Admin models
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from utilities.admin import ArticleBaseAdmin

from . import models


@admin.decorators.register(models.NewsItem)
class ProjectAdmin(ArticleBaseAdmin):
    """
    A project admin
    """
    list_display = ("thumb_html", "published", "title", "slug", "created",
                    "updated", "published_on")
    list_display_links = ("thumb_html", "title")
    list_editable = ("published",)
    list_filter = ("published", "published_on", "created", "updated")
    list_per_page = 10

    fieldsets = [
        (None, {
            "fields": (
                "title",
                ("published", "published_on"),
                "teaser",
                ("thumb_html", "image"),
            ),
        }),
        (_("Advanced options"), {
            "fields": ("slug", ("created", "updated")),
            "classes": ("collapse",),
        })
    ]

    readonly_fields = ("created", "updated", "thumb_html", "published_on")
