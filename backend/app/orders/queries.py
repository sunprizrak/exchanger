import graphene
from .models import Order
from .types import OrderType


class Query(graphene.ObjectType):
    order = graphene.Field(OrderType)

    def resolve_order(root, info):
        return Order.objects.first()