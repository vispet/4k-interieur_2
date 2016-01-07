"""
Home admin
"""

from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import Settings


@admin.decorators.register(Settings)
class SettingsAdmin(SingletonModelAdmin):
    """
    Homepage admin stub
    """
    pass
