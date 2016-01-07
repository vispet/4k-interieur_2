"""
Views
"""

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Project


def index(request, page=None):
    """
    Get some results
    """
    if page is not None and int(page) == 1:
        return redirect("portfolio:index")

    paginator = Paginator(Project.objects.filter(active=True), 17,
                          orphans=3)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        raise Http404()

    return render(request, "portfolio/index.html", {
        "projects": projects,
    })


def project(request, slug):
    """
    Render a portfolio project
    """
    return render(request, "portfolio/project.html", {
        "project": get_object_or_404(Project, active=True, slug=slug),
    })
