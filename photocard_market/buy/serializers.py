from product.serializers import PhotoCardListSerializer
from rest_framework import serializers
from sale.models import SaleHistory


class BuyRequestSerializer(serializers.ModelSerializer):
    buyer = serializers.IntegerField(read_only=True)

    class Meta:
        model = SaleHistory
        fields = [
            "id",
            "buyer",
        ]


class BuyListSerializer(serializers.ModelSerializer):
    photo_card = PhotoCardListSerializer(read_only=True)
    state = serializers.SerializerMethodField()

    class Meta:
        model = SaleHistory
        fields = ["id", "price", "state", "sold_date", "photo_card"]

    def get_state(self, value):
        return value.get_state_display().replace("판매", "거래")
