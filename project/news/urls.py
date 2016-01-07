"""
Urls
"""
from django.conf.urls import url

from . import views

app_name = "news"  # pylint: disable=invalid-name
urlpatterns = [  # pylint: disable=invalid-name
    url(r"^$", views.index, name="index"),
    url(r"^(?P<page>\d+)/$", views.index, name="page"),
    url(r"^(?P<slug>[a-z0-9-]+)/$", views.project, name="item"),
]
