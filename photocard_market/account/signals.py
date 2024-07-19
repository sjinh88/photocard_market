from django.db.models.signals import post_save
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import User, UserWallet


@receiver(post_save, sender=User)
def add_user_wallet(sender, instance, created, **kwargs):
    """
    회원가입 시 지갑 정보를 생성해준다.
    - 회원가입 시 10,000 캐시 지급
    """
    if created:
        UserWallet.objects.create(user=instance)


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'account':  # 특정 앱에 대해서만 실행
        password = 'admin'
        email = 'admin@admin.com'

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)