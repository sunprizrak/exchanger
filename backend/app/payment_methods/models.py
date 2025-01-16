from django.db import models


def path_coin_icon(instance, filename):
    return 'currency/icons/{currency_name}-{filename}'.format(
        currency_name=instance.name,
        filename=filename,
    )


class Currency(models.Model):
    code = models.CharField(verbose_name="Код валюты", max_length=3, unique=True, )  # BYN, RUB, etc.
    name = models.CharField(verbose_name="Название", max_length=50)  # Dollar, Euro, etc.
    icon = models.ImageField(verbose_name="Иконка", upload_to=path_coin_icon, default='default_image.png', blank=True)
    symbol = models.CharField(max_length=10, blank=True, verbose_name="Символ валюты")  # $, €, etc.

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return f"{self.name} ({self.code})"


class PaymentMethod(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50, unique=True, )  # PayPal, Credit Card, etc.
    description = models.TextField(verbose_name="Описание", blank=True, null=True, )
    currencies = models.ManyToManyField(Currency, verbose_name="Поддерживаемые валюты", related_name="payment_methods")

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"

    def __str__(self):
        return self.name
