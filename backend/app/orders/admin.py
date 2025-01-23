from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "coin_name",
        "coin_ticker",
        "coin_amount",
        "currency",
        "currency_code",
        "total_price",
        "payment_method",
        "status",
    )
