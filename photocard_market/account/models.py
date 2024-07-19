from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
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
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(
        unique=True, max_length=13, null=False, help_text="핸드폰 번호"
    )
    nickname = models.CharField(
        unique=True, max_length=13, null=False, help_text="닉네임"
    )

    create_date = models.DateTimeField(auto_now_add=True, help_text="생성 일자")
    update_date = models.DateTimeField(auto_now=True, help_text="정보 변경 일자")

    class Meta:
        indexes = [
            models.Index(fields=["-create_date"]),
        ]


class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    cash = models.PositiveIntegerField(default=10000, help_text="사용가능 금액")

    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
