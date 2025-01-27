import graphene
from django.utils.timezone import localtime
from graphene_django import DjangoObjectType
from .models import Order


class OrderType(DjangoObjectType):
    created_formatted = graphene.String()

    class Meta:
        model = Order

    def resolve_created_formatted(self, info):
        # Преобразуем дату/время в нужный формат
        return localtime(self.created).strftime("%d.%m.%Y %H:%M")