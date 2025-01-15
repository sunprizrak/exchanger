import graphene
from .models import Coin
from .types import CoinType


# class CreateOrder(graphene.Mutation):
#     order = graphene.Field(CoinType)
#
#     class Arguments:
#         coin_name = graphene.String(required=True)
#         coin_amount = graphene.Decimal(required=True)
#         total_price = graphene.Decimal(required=True)
#
#     def mutate(self, info, coin_name, coin_amount, total_price):
#         # Получаем текущего пользователя (если вы хотите, чтобы заказ был привязан к пользователю)
#         user = info.context.user
#
#         # Создаем новый заказ
#         order = Order.objects.create(
#             user=user,
#             coin_name=coin_name,
#             coin_amount=coin_amount,
#             total_price=total_price,
#         )
#
#         return CreateOrder(order=order)
#
#
# class Mutation(graphene.ObjectType):
#     create_order = CreateOrder.Field()