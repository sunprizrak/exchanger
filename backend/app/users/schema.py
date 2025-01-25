import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.utils import jwt_payload
from .queries import Query
from .mutations import Mutation


def custom_jwt_payload(user, context):
    payload = jwt_payload(user, context)
    payload['tg_id'] = user.tg_id
    return payload


def custom_get_user_by_natural_key_handler(key):
    user_model = get_user_model()
    try:
        return user_model._default_manager.get_by_natural_key(telegram_id=key)
    except user_model.DoesNotExist:
        return None


schema = graphene.Schema(query=Query, mutation=Mutation)