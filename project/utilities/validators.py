"""
Custom validators
"""

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

validate_slug_lower = RegexValidator(  # pylint: disable=invalid-name
    r"^[-a-z0-9]+\Z",
    _("Enter a valid 'slug' consisting of lowercase letters, numbers or "
      "hyphens."),
    "invalid"
)

validate_phone = RegexValidator(  # pylint: disable=invalid-name
    r"^\+?1?\d{9,15}$",
    _("Phone number must be entered in the format: '+999999999'. Up to 15 "
      "digits allowed.")
)

validate_btw = RegexValidator(  # pylint: disable=invalid-name
    r"^\d{9}$",
    _("Gelieve een nummer van 9 cijfers in te voeren zonder het BE "
      "voorvoegsel.")
)
