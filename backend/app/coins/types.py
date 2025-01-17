import graphene
from django.conf import settings
from graphene_django import DjangoObjectType

from .models import Coin


class CoinType(DjangoObjectType):
    full_icon_url = graphene.String()

    class Meta:
        model = Coin

    def resolve_full_icon_url(self, info):
        """Этот метод будет возвращать полный URL для иконки."""
        if self.icon:
            return f"{settings.SITE_URL}{self.icon.url}"
        return None