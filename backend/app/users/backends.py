from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


UserModel = get_user_model()


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, tg_id=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
            if username is None:
                username = tg_id
        if username is None or password is None:
            return None

        # Попробуем найти пользователя по tg_id или email
        user = UserModel._default_manager.filter(
            Q(tg_id=username) | Q(email=username)
        ).first()

        if user is None:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None