import graphene
from .models import User
from .types import UserType


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)

    def resolve_user(root, info):
        return User.objects.first()