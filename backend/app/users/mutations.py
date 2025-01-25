import graphene
import graphql_jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from .types import UserType
from graphql_jwt.shortcuts import get_token
from .utility import verify_telegram_data


UserModel = get_user_model()


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class TelegramAuth(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        init_data = graphene.String(required=True)

    def mutate(root, info, init_data):
        token_tg = settings.TELEGRAM_BOT_TOKEN

        # Проверка валидности данных Telegram
        user_data = verify_telegram_data(token=token_tg, init_data=init_data)

        if not user_data:
            raise Exception("Недействительные данные Telegram.")

        telegram_id, username = user_data

        user, created = UserModel.objects.get_or_create(
            tg_id=telegram_id,
            defaults={"tg_username": username},
        )

        # Выдача токена
        token_jwt = get_token(user)
        return TelegramAuth(user=user, token=token_jwt)


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    telegram_auth = TelegramAuth.Field()