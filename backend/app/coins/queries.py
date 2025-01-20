import graphene
from .models import Coin
from .types import CoinType
from graphql import GraphQLError

from .utility import calculate_coin_amount


class Query(graphene.ObjectType):
    # Получение монеты по тикеру
    coin = graphene.Field(CoinType, ticker=graphene.String(required=True))
    # Поле для запроса количества монет
    coins_amount = graphene.Field(
        graphene.Float,
        amount=graphene.Float(required=True),
        currency_code=graphene.String(required=True),
        coin_ticker=graphene.String(required=True),
    )

    def resolve_coin(root, info, ticker):
        try:
            return Coin.objects.get(ticker=ticker)
        except Coin.DoesNotExist:
            return None

    # Получение всех монет
    all_coins = graphene.List(CoinType)

    def resolve_all_coins(root, info):
        return Coin.objects.all()

    def resolve_coins_amount(self, info, amount, currency_code, coin_ticker):
        try:
            # Рассчитываем количество монет
            return calculate_coin_amount(amount, currency_code, coin_ticker)
        except Exception as e:
            raise GraphQLError(f"Ошибка: {str(e)}")