# Generated by Django 5.1.4 on 2025-01-22 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=50, null=True, verbose_name='Платёжный метод'),
        ),
    ]
