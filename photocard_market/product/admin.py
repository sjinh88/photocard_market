from django.contrib import admin

from .models import PhotoCard


@admin.register(PhotoCard)
class PhotoCardAdmin(admin.ModelAdmin):
    list_display = ["name", "photo_card", "description", "create_date", "update_date"]
    search_fields = ["name"]
