"""
Admin models
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from adminsortable.admin import SortableAdmin

from utilities.admin import ArticleBaseAdmin

from . import models


@admin.decorators.register(models.Project)
class ProjectAdmin(ArticleBaseAdmin, SortableAdmin):
    """
    A project admin
    """
    list_display = ("thumb_html", "active", "title", "slug", "created",
                    "updated")
    list_display_links = ("thumb_html", "title")
    list_editable = ("active",)
    list_filter = ("active", "created", "updated")
    list_per_page = 10

    fieldsets = [
        (None, {
            "fields": (
                ("title", "active"),
                "teaser",
                ("thumb_html", "image"),
            ),
        }),
        (_("Advanced options"), {
            "fields": ("slug", "created", "updated"),
            "classes": ("collapse",),
        })
    ]

    readonly_fields = ("created", "updated", "thumb_html")
