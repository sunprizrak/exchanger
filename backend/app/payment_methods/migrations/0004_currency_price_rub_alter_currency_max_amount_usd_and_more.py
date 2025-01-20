# Generated by Django 5.1.4 on 2025-01-20 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_methods', '0003_currency_max_amount_usd_currency_min_amount_usd_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='price_rub',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True, verbose_name='Цена в RUB'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='max_amount_usd',
            field=models.DecimalField(blank=True, decimal_places=2, default=10000, max_digits=50, verbose_name='Макс. сумма в USD'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='min_amount_usd',
            field=models.DecimalField(blank=True, decimal_places=2, default=10, max_digits=50, verbose_name='Мин. сумма в USD'),
        ),
    ]
