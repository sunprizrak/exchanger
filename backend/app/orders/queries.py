import graphene
from .models import Order
from .types import OrderType
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    # Получение всех ордеров
    all_orders = graphene.List(OrderType)

    @login_required
    def resolve_all_orders(root, info):
        user = info.context.user
        return Order.objects.filter(user=user)