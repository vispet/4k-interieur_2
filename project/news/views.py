"""
Views
"""

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import NewsItem


def index(request, page=None):
    """
    Get some results
    """
    return render(request, "news/index.html", {
        "page": page,
    })


def project(request, slug):
    """
    Render a portfolio project
    """
    return render(request, "news/item.html", {
        "project": get_object_or_404(NewsItem, published=True, slug=slug),
    })
