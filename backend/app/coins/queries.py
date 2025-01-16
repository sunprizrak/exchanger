import graphene
from .models import Coin
from .types import CoinType


class Query(graphene.ObjectType):
    # Получение монеты по тикеру
    coin = graphene.Field(CoinType, ticker=graphene.String(required=True))

    def resolve_order(root, info, ticker):
        try:
            return Coin.objects.get(ticker=ticker)
        except Coin.DoesNotExist:
            return None

    # Получение всех монет
    all_coins = graphene.List(CoinType)

    def resolve_all_coins(root, info):
        return Coin.objects.all()