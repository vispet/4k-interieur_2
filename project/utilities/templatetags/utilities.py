"""
Utilities
"""

import re

from django import template
from django.utils.translation import to_locale
from django.core.urlresolvers import reverse

from ..columnizer import get_best_pattern

register = template.Library()  # pylint: disable=invalid-name


@register.filter("to_locale")
def to_locale_filter(content):
    """
    Convert the language code to a locale code
    """
    return to_locale(content)


@register.filter
def strip_newlines(content):
    """
    Strip newlines from string
    """
    return content.replace("\n", " ")


@register.filter
def active_url(request, reversible):
    """
    Test if the url is active
    """
    return request.get_full_path().startswith(reverse(reversible))


@register.filter
def active_url_strict(request, reversible):
    """
    Test if url is equal
    """
    return request.get_full_path() == reverse(reversible)


@register.filter
def format_phone(phone):
    """
    Format a phone
    """
    formatted = re.sub(r"^(\+\d{2}).*", r"\1 (0)", phone)
    formatted += "%s " % phone[:-6][3:]
    formatted += "%s %s %s" % (
        phone[-6:-4],
        phone[-4:-2],
        phone[-2:]
    )
    return formatted


@register.filter
def format_btw(btw):
    """
    Format btw num
    """
    return "BE %s.%s.%s" % (btw[:2], btw[3:5], btw[6:])


@register.simple_tag(takes_context=True)
def column(context, nodes_length, tier, max_available):
    """
    Create a column class
    """
    if "_columnizer-cache" not in context:
        context["_columnizer-cache"] = {}

    cache = context["_columnizer-cache"]
    key = "%i%i" % (max_available, nodes_length)

    if key not in cache:
        cache[key] = get_best_pattern(max_available, nodes_length)

    pattern = cache[key]

    idx = context["forloop"]["counter0"]
    pattern_idx = 0
    counter = 0

    while(idx > 0):
        idx -= 1
        counter += 1
        if counter >= pattern[pattern_idx]:
            pattern_idx += 1
            counter = 0
        if pattern_idx >= len(pattern):
            pattern_idx = 0

    return "col-%s-%i" % (tier, 12 / pattern[pattern_idx])


@register.inclusion_tag("inc/pagination.html")
def pagination(page, index_url_pattern, page_url_pattern):
    """
    Renders the pagination
    """
    previous_href = None
    if page.number == 1:
        previous_href = reverse(index_url_pattern)
    else:
        previous_href = reverse(page_url_pattern, kwargs={
            "page": page.previous_page_number()
        })

    next_href = None
    if page.has_next():
        next_href = reverse(page_url_pattern, kwargs={
            "page": page.next_page_number()
        })

    return {
        "page": page,
        "previous_href": previous_href,
        "next_href": next_href,
        "index_url_pattern": index_url_pattern,
        "page_url_pattern": page_url_pattern,
    }
