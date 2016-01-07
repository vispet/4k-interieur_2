"""
General context processors
"""

from django.conf import settings


def google_analytics(dummy_request):
    """
    fetch the google analytics id and add it to the context
    """
    return {
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
    }
