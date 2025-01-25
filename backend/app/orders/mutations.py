from graphql_jwt.decorators import login_required
from .models import Order
from .types import OrderType
import graphene
import logging


logger = logging.getLogger(__name__)


class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)
    message = graphene.String()

    class Arguments:
        coin_name = graphene.String(required=True)
        coin_ticker = graphene.String(required=True)
        coin_amount = graphene.Float(required=True)
        currency = graphene.String(required=True)
        currency_code = graphene.String(required=True)
        total_price = graphene.Float(required=True)
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
        logger.error("Context Headers:")
        for key, value in info.context.META.items():
            if key.startswith('HTTP_'):  # HTTP заголовки
                logger.error(f"{key}: {value}")

        logger.error(f"User: {user}")

        # Если пользователя нет (не аутентифицирован)
        if not user or not user.is_authenticated:
            logger.error("User is not authenticated.")
            raise Exception("Пользователь не аутентифицирован")

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

        # Значение для поля message
        message = "Ваша заявка принята"

        return CreateOrder(order=order, message=message)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()