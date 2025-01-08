from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    coin_name = models.CharField(verbose_name='Название', max_length=255)
    coin_amount = models.DecimalField(verbose_name='Количество', max_digits=10, decimal_places=2)
    total_price = models.DecimalField(verbose_name='Итоговая Цена', max_digits=10, decimal_places=2)
    status = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='pending',
    )
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    def tg_id(self):
        return self.user.tg_id  # Возвращаем tg_id из пользователя

    def tg_username(self):
        return self.user.tg_username

    def __str__(self):
        return f'order {self.id}'

    class Meta:
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордера'