from graphene_django import DjangoObjectType
from .models import Coin


class CoinType(DjangoObjectType):
    class Meta:
        model = Coin