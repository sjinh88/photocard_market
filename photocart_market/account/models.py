from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        PermissionsMixin, UserManager)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = AccountManager()

    EMAIL_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(unique=True, max_length=13, null=False)
    nickname = models.CharField(unique=True, max_length=13, null=False)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["-create_date"]),
        ]


class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    cash = models.PositiveIntegerField(default=10000)

    update_date = models.DateTimeField(auto_now=True)
