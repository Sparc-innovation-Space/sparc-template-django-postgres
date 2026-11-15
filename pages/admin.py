"""Models listed here can be edited at /admin (log in with the user from `createsuperuser`, see README)."""
from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at")
    search_fields = ("text",)
