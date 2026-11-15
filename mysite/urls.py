"""Which address shows which page. Add a page: write a view in pages/views.py and add a line here."""
from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
]
