import graphene
from .models import Coin
from .types import CoinType
from graphql import GraphQLError


class Query(graphene.ObjectType):
    # Получение монеты по тикеру
    coin = graphene.Field(CoinType, ticker=graphene.String(required=True))
    # Поле для запроса количества монет
    get_coin_amount = graphene.Float(amount=graphene.Float(), currency_code=graphene.String(), coin_ticker=graphene.String())


    def resolve_order(root, info, ticker):
        try:
            return Coin.objects.get(ticker=ticker)
        except Coin.DoesNotExist:
            return None

    # Получение всех монет
    all_coins = graphene.List(CoinType)

    def resolve_all_coins(root, info):
        return Coin.objects.all()

    def resolve_get_coin_amount(self, info, amount, currency_code, coin_ticker):
        try:
            # Находим монету по тикеру
            coin = Coin.objects.get(ticker=coin_ticker)
            # Рассчитываем количество монет
            return coin.calculate_coin_amount(amount, currency_code)
        except Coin.DoesNotExist:
            raise GraphQLError(f"Монета с тикером {coin_ticker} не найдена.")
        except Exception as e:
            raise GraphQLError(f"Ошибка при расчёте: {str(e)}")