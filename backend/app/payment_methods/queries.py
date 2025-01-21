import graphene
from graphql import GraphQLError
from utility.payment_methods import calculate_currency_amount
from .models import Currency
from .types import CurrencyType


class Query(graphene.ObjectType):
    all_currencies = graphene.List(CurrencyType)
    currency_amount = graphene.Field(
        graphene.Float,
        amount=graphene.Float(required=True),
        currency_code=graphene.String(required=True),
        coin_ticker=graphene.String(required=True),
    )

    def resolve_all_currencies(root, info):
        # Загружаем все валюты с предзагруженными методами оплаты
        return Currency.objects.prefetch_related('payment_methods').all()

    def resolve_currency_amount(root, info, amount, currency_code, coin_ticker):
        try:
            # Рассчитываем количество монет
            return calculate_currency_amount(amount, currency_code, coin_ticker)
        except Exception as e:
            raise GraphQLError(f"Ошибка: {str(e)}")