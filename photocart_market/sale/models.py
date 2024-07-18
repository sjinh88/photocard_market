from account.models import User
from django.db import models
from product.models import PhotoCard


class SaleHistory(models.Model):

    class State(models.TextChoices):
        END = "E", "판매완료"
        BEGIN = "B", "판매중"
        START = "S", "등록"

    photo_card = models.ForeignKey(
        PhotoCard, related_name="photocard", on_delete=models.DO_NOTHING
    )
    buyer = models.ForeignKey(
        User, related_name="buy_user", on_delete=models.DO_NOTHING, null=True
    )
    seller = models.ForeignKey(
        User, related_name="sale_user", on_delete=models.DO_NOTHING
    )

    price = models.PositiveIntegerField(help_text="1개당 가격")
    fee = models.PositiveIntegerField()

    state = models.CharField(choices=State.choices, max_length=1, default=State.START)

    create_date = models.DateTimeField(auto_now_add=True)
    renewal_date = models.DateTimeField(null=True)
    sold_date = models.DateTimeField(null=True)

    class Meta:
        ordering = [
            "photo_card_id",
            "price",
            "renewal_date",
            "id",
        ]
