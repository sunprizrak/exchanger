import graphene
from .models import Coin
from .types import CoinType


class Query(graphene.ObjectType):
    order = graphene.Field(CoinType)

    def resolve_order(root, info):
        return Coin.objects.first()