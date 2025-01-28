import graphene
from .models import Order
from .types import OrderType
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    # Получение всех ордеров
    all_orders = graphene.List(OrderType)
    order_status = graphene.String(order_id=graphene.ID(required=True))

    @login_required
    def resolve_all_orders(root, info):
        user = info.context.user
        return Order.objects.filter(user=user).order_by('-created')

    @login_required
    def resolve_order_status(self, info, order_id):
        # Получаем ордер по ID
        try:
            order = Order.objects.get(id=order_id)
            return order.status
        except Order.DoesNotExist:
            return None  # Если ордер не найден, возвращаем None