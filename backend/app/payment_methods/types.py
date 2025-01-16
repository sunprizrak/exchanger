import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from .models import Currency, PaymentMethod


class PaymentMethodType(DjangoObjectType):

    class Meta:
        model = PaymentMethod


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