"""The pages. Each function gets a request and returns a page."""
from django.shortcuts import render

from .models import Note


def home(request):
    return render(request, "pages/home.html", {"notes": Note.objects.all()[:20]})
