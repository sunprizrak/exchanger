import graphene
from django.contrib.auth import get_user_model
from .types import UserType
import graphql_jwt

UserModel = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        tg_id = graphene.String(required=True)
        tg_username = graphene.String(required=True)

    def mutate(self, info, tg_id, tg_username):
        print('hello mutate')
        obj = UserModel.objects.create_user(tg_id=tg_id, tg_username=tg_username)
        return CreateUser(user=obj)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()