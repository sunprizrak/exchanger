from django.db import models


def path_coin_icon(instance, filename):
    return 'coins/icons/{coin_id}-{coin_name}-{coin_ticker}-{filename}'.format(
        coin_id=instance.id,
        coin_name=instance.name,
        coin_ticker=instance.ticker,
        filename=filename,
    )


class Coin(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255, unique=True)
    ticker = models.CharField(verbose_name='Тикер', max_length=255, unique=True)
    icon = models.ImageField(verbose_name='Иконка', upload_to=path_coin_icon, default='coins/icons/default_image.png', blank=True)
    price_usd = models.DecimalField(verbose_name='Цена USD', max_digits=10, decimal_places=2, null=True, blank=True)
    price_rub = models.DecimalField(verbose_name='Цена RUB', max_digits=10, decimal_places=2, null=True, blank=True)
    price_byn = models.DecimalField(verbose_name='Цена BYN', max_digits=10, decimal_places=2, null=True, blank=True)
    commission_rate = models.DecimalField(
        verbose_name='Комиссия',
        max_digits=5,
        decimal_places=2,
        default=9,
    )

    class Meta:
        verbose_name = "Монета"
        verbose_name_plural = "Монеты"

    def __str__(self):
        return self.name

