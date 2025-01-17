from decimal import Decimal

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
    price_usd = models.DecimalField(
        verbose_name="Цена в USD",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    # Новые поля для минимальной и максимальной суммы
    min_amount = models.DecimalField(
        verbose_name="Мин. сумма в эквиваленте USD",
        max_digits=10,
        decimal_places=2,
        default=10,
        blank=True,
    )
    max_amount = models.DecimalField(
        verbose_name="Макс. сумма в эквиваленте USD",
        max_digits=10,
        decimal_places=2,
        default=10000,
        blank=True,
    )

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def calculate_min_max(self):
        """
        Метод для расчета минимальной и максимальной суммы для валюты, основываясь на курсе USD.
        """
        if self.price_usd is not None and self.price_usd > 0:
            # Минимальная и максимальная сумма в локальной валюте
            self.min_amount = Decimal(self.min_amount) * self.price_usd
            self.max_amount = Decimal(self.min_amount) * self.price_usd
            self.save()

    def update_exchange_rate(self, new_price_usd):
        """
        Обновляет курс USD для валюты и пересчитывает минимальные и максимальные суммы в эквиваленте USD.
        """
        self.price_usd = new_price_usd
        self.calculate_min_max()

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
