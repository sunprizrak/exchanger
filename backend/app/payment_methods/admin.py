from django.contrib import admin
from .models import Currency, PaymentMethod


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name",
                    "code",
                    "symbol",
                    "price_usd",
                    "price_rub",
                    "min_amount_usd",
                    "max_amount_usd",
                    "min_amount",
                    "max_amount",
                    "get_payment_methods"
                    )
    search_fields = ("name", "code")

    def get_payment_methods(self, obj):
        # Возвращает связанные способы оплаты в виде строки
        return ", ".join([method.name for method in obj.payment_methods.all()])
    get_payment_methods.short_description = "Способы оплаты"  # Подпись столбца в админке


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "get_currencies")  # Отображение валют, с которыми связан способ оплаты
    search_fields = ("name",)

    def get_currencies(self, obj):
        # Возвращает связанные валюты в виде строки
        return ", ".join([currency.name for currency in obj.currencies.all()])
    get_currencies.short_description = "Валюты"  # Подпись столбца в админке
