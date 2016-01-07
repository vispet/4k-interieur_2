"""
Main url definition module
"""

from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from portfolio import urls as portfolio_urls
from news import urls as news_urls
from home import urls as home_urls
from about import urls as about_urls
from contact import urls as contact_urls

urlpatterns = [  # pylint: disable=invalid-name
    url(r"^", include(home_urls)),
    url(r"^about/", include(about_urls)),
    url(r"^contact/", include(contact_urls)),
    url(r"^portfolio/", include(portfolio_urls)),
    url(r"^nieuws/", include(news_urls)),
    url(r"^admin/", include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
