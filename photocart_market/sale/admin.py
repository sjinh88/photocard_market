from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .models import SaleHistory

@admin.register(SaleHistory)
class SaleHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "photo_card",
        "seller",
        "buyer",
        "price",
        "fee",
        "state",
        "renewal_date",
        "sold_date"
    ]
    ordering = [
        "-create_date",
    ]
    list_display_links = [
        "photo_card",
        "seller",
        "buyer",
    ]

