"""
Configuration models
"""

import urllib

from django.db import models

from solo.models import SingletonModel

from utilities.validators import validate_phone
from utilities.validators import validate_btw

_ICONS = {
    "email": "fontello-mail",
    "facebook": "fontello-facebook",
    "twitter": "fontello-twitter",
    "instagram": "fontello-instagram",
    "pinterest": "fontello-pinterest-circled",
}


class GeneralSettings(SingletonModel):
    """
    Global configuration settings
    """
    # Social
    email = models.EmailField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    pinterest = models.URLField(null=True, blank=True)

    # Mailto
    subject = models.CharField(null=True, blank=True, max_length=255)
    body = models.TextField(null=True, blank=True)

    # Extra
    phone = models.CharField(max_length=15, validators=[validate_phone],
                             null=True, blank=True)
    btw = models.CharField(max_length=9, validators=[validate_btw], null=True,
                           blank=True)

    @property
    def mailto(self):
        """
        Format a mailto link
        """
        if not self.email:
            return None

        base = "mailto:%s" % self.email

        if not self.subject:
            return base

        link = "%s?" % base
        parameters = {}
        if self.subject:
            parameters["subject"] = urllib.quote(self.subject)
        if self.body:
            parameters["body"] = urllib.quote(self.body)
        link += "&".join(
            ["%s=%s" % (key, value) for key, value in parameters.iteritems()])
        return link

    @property
    def social(self):
        """
        Test social
        """
        for link in ("facebook", "twitter", "instagram", "pinterest", "email"):
            url = getattr(self, link)
            if url:
                if link == "email":
                    url = self.mailto
                yield {
                    "url": url,
                    "class": _ICONS[link],
                }
