from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group as BaseGroup
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class Group(BaseGroup):

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email address'), unique=True, null=True, blank=True)
    tg_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    tg_username = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        ordering = ['-created']
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        if self.is_superuser:
            return self.email
        else:
            return f'{self.tg_username} {self.tg_id}'