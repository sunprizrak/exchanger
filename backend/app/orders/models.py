from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def path_check_img(instance, filename):
    return 'orders/check/{order_id}-{tg_id}-{filename}'.format(
        order_id=instance.id,
        tg_id=instance.user.tg_id,
        filename=filename,
    )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    coin_name = models.CharField(verbose_name='Название', max_length=50)
    coin_ticker = models.CharField(verbose_name='Tикер', max_length=50, null=True)
    coin_amount = models.DecimalField(verbose_name='Количество', max_digits=10, decimal_places=2)
    total_price = models.DecimalField(verbose_name='Итоговая Цена', max_digits=10, decimal_places=2)
    currency = models.CharField(verbose_name="Валюта", max_length=50, null=True)
    currency_code = models.CharField(verbose_name="Код валюты", max_length=3, null=True)
    payment_method = models.CharField(verbose_name="Платёжный метод", max_length=50, null=True)
    status = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='pending',
    )
    foto_check = models.ImageField(verbose_name='Чек', upload_to=path_check_img, null=True, blank=True)
    wallet = models.CharField(verbose_name='Кошелёк', max_length=250, null=True, blank=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    def tg_id(self):
        return self.user.tg_id

    def tg_username(self):
        return self.user.tg_username

    def __str__(self):
        return f'order {self.id}'

    class Meta:
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордера'