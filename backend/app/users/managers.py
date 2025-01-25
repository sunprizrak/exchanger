from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .utility import generate_random_password


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_with_telegram(self, tg_id, tg_username, **extra_fields):
        print(tg_id)
        if not tg_id:
            raise ValueError(_('The Telegram_id must be set'))
        user = self.model(tg_id=tg_id, tg_username=tg_username, **extra_fields)
        password = generate_random_password()
        user.set_password(password)
        user.save()
        return user

    def _create_with_email(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, tg_id, tg_username, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_with_telegram(tg_id, tg_username, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_with_email(email, password, **extra_fields)

    def get_by_natural_key(self, username=None, telegram_id=None):
        if telegram_id:
            try:
                return self.get(tg_id=telegram_id)
            except self.model.DoesNotExist:
                return None
        elif username:
            return super().get_by_natural_key(username)