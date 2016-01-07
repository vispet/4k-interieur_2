"""
Urls
"""

from django.conf.urls import url
from django.views.generic import TemplateView


app_name = "contact"  # pylint: disable=invalid-name
urlpatterns = [  # pylint: disable=invalid-name
    url(r"^$", TemplateView.as_view(template_name="contact.html"),
        name="index"),
]
