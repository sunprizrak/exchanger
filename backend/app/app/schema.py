import graphene
from graphql_jwt.utils import jwt_payload
from users.schema import schema as users_schema
from users.mutations import Mutation as users_mutations
from orders.schema import schema as orders_schema
from orders.mutations import Mutation as orders_mutations
from coins.schema import schema as coins_schema
from payment_methods.schema import schema as payment_methods_schema


def custom_jwt_payload(user, context):
    payload = jwt_payload(user, context)
    payload['tg_id'] = user.tg_id
    return payload


# Объединяем Query
class Query(
    users_schema.Query,
    orders_schema.Query,
    coins_schema.Query,
    payment_methods_schema.Query,
    graphene.ObjectType

):
    pass  # Здесь можно добавить дополнительные поля, если нужно


# Объединение мутаций
class Mutation(users_mutations, orders_mutations, graphene.ObjectType):
    pass  # Мы можем добавить дополнительные мутации, если нужно


# Главная схема, которая объединяет все
schema = graphene.Schema(query=Query, mutation=Mutation)