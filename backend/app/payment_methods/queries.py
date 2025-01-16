import graphene
from .models import Currency
from .types import CurrencyType


class Query(graphene.ObjectType):
    all_currencies = graphene.List(CurrencyType)

    def resolve_all_currencies(root, info):
        # Загружаем все валюты с предзагруженными методами оплаты
        return Currency.objects.prefetch_related('payment_methods').all()