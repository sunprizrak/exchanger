from django.db import models


class Coin(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    price_rub = models.DecimalField(verbose_name='Цена RUB', max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(
        verbose_name='Комиссия',
        max_digits=5,
        decimal_places=2,
        default=9,
    )

    def __str__(self):
        return self.name

class Monero(Coin):

    def clean(self):
        """Ограничиваем количество объектов до одного."""
        if Monero.objects.exists() and not self.pk:
            from django.core.exceptions import ValidationError
            raise ValidationError("Можно создать только один экземпляр Monero.")

    def save(self, *args, **kwargs):
        # Вызываем clean() перед сохранением
        self.clean()
        super(Monero, self).save(*args, **kwargs)

