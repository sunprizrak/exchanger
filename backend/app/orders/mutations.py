from decimal import Decimal

from graphql_jwt.decorators import login_required
from .models import Order
from .types import OrderType
import graphene
import logging


logger = logging.getLogger(__name__)


class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        coin_name = graphene.String(required=True)
        coin_ticker = graphene.String(required=True)
        coin_amount = graphene.String(required=True)
        currency = graphene.String(required=True)
        currency_code = graphene.String(required=True)
        total_price = graphene.String(required=True)
        payment_method = graphene.String(required=True)

    @login_required
    def mutate(
            root,
            info,
            coin_name,
            coin_ticker,
            coin_amount,
            currency,
            currency_code,
            total_price,
            payment_method
    ):
        user = info.context.user  # Получаем текущего пользователя

        # Создаем новый заказ
        order = Order.objects.create(
            user=user,
            coin_name=coin_name,
            coin_ticker=coin_ticker,
            coin_amount=coin_amount,
            currency=currency,
            currency_code=currency_code,
            total_price=total_price,
            payment_method=payment_method,
        )

        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()