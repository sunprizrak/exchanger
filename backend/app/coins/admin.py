from django.contrib import admin
from .models import Coin


@admin.register(Coin)
class CoinsAdmin(admin.ModelAdmin):
    list_display = ("name", "ticker", "price_usd", "price_rub", "price_byn", "commission_rate")
