"""
Configuration admin
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from solo.admin import SingletonModelAdmin

from .models import GeneralSettings


@admin.decorators.register(GeneralSettings)
class GeneralSettingsAdmin(SingletonModelAdmin):
    """
    Settings admin
    """
    fieldsets = (
        (_("Email"), {
            "classes": ("collapse",),
            "fields": ("email", "subject", "body"),
        }),
        (_("Social"), {
            "classes": ("collapse",),
            "fields": ("facebook", "twitter", "instagram", "pinterest"),
        }),
        (_("Administratief"), {
            "classes": ("collapse",),
            "fields": ("phone", "btw"),
        }),
    )
