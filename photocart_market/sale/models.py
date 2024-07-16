from django.db import models
from account.models import User
from register.models import PhotoCard

class SaleHistory(models.Model):
    
    class State(models.TextChoices):
        END = "E", "판매완료"
        BEGIN = "B", "판매중"
    
    photo_card = models.ForeignKey(PhotoCard, on_delete=models.DO_NOTHING)
    ea = models.PositiveSmallIntegerField(default=1)
    
    buyer = models.ForeignKey(User, related_name="buy_user", on_delete=models.DO_NOTHING, null=True)
    seller = models.ForeignKey(User, related_name="sale_user", on_delete=models.DO_NOTHING)
    
    price = models.PositiveIntegerField()
    fee = models.PositiveIntegerField()
    
    state = models.CharField(choices=State.choices, max_length=1)
    
    create_date = models.DateTimeField(auto_now_add=True)
    renewal_date = models.DateTimeField(null=True)
    sold_date = models.DateTimeField(null=True)
    
    