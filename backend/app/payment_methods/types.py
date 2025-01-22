import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from .models import Currency, PaymentMethod


class PaymentMethodType(DjangoObjectType):
    full_icon_url = graphene.String()

    class Meta:
        model = PaymentMethod

    def resolve_full_icon_url(self, info):
        """Этот метод будет возвращать полный URL для иконки."""
        if self.icon:
            return f"{settings.SITE_URL}{self.icon.url}"
        return None


class CurrencyType(DjangoObjectType):
    full_icon_url = graphene.String()
    payment_methods = graphene.List(PaymentMethodType)

    class Meta:
        model = Currency

    def resolve_full_icon_url(self, info):
        """Этот метод будет возвращать полный URL для иконки."""
        if self.icon:
            return f"{settings.SITE_URL}{self.icon.url}"
        return None

    def resolve_payment_methods(self, info):
        """Возвращаем итерабельный список способов оплаты."""
        return self.payment_methods.all()