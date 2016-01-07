"""
Urls
"""

from django.conf.urls import url
from django.views.generic import TemplateView


app_name = "about"  # pylint: disable=invalid-name
urlpatterns = [  # pylint: disable=invalid-name
    url(r"^$", TemplateView.as_view(template_name="about.html"), name="index"),
]
