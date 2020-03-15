from django.contrib import admin

from .models import Room

admin.site.register(
    Room,
    list_display=["id", "name", "staff_only", "historical_count", "historical_period"],
    list_display_links=["id", "name"],
)
