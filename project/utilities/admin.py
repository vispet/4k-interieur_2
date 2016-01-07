"""
Admin models
"""

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from simple_resizer import resize_lazy

from feincms.admin.item_editor import ItemEditor


class ArticleBaseAdmin(ItemEditor):
    """
    Item editor for abstract model base
    """
    save_on_top = True

    search_fields = ("title", "teaser")
    prepopulated_fields = {"slug": ("title",)}

    def thumb_html(self, obj=None):  # pylint: disable=no-self-use
        """
        Get the html for a thumb of a project
        """
        if obj is None:
            return None
        return mark_safe("<img src=\"%s\" />" % resize_lazy(
            obj.image, 100, 100, True, as_url=True))
    thumb_html.short_description = _("Thumbnail")
