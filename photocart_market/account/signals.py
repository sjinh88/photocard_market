from django.db.models.signals import post_save
from .models import User, UserWallet
from django.dispatch import receiver

@receiver(post_save, sender=User)
def add_user_wallet(sender, instance, created, **kwargs):
    """
    회원가입 시 지갑 정보를 생성해준다.
    - 회원가입 시 10,000 캐시 지급
    """
    if created:
        UserWallet.objects.create(user=instance)