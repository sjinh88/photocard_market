from rest_framework import serializers

from .models import SaleHistory


class SaleHistorySerializer(serializers.ModelSerializer):
    """
    판매 내역 serializer
    """

    state = serializers.SerializerMethodField()

    class Meta:
        model = SaleHistory
        fields = ["id", "photo_card_id", "price", "renewal_date", "sold_date", "state"]

    def get_state(self, value):
        return value.get_state_display()


class SaleResigterSerializer(SaleHistorySerializer):
    """
    판매 등록 serializer
    """

    seller = serializers.CharField(read_only=True)
    fee = serializers.IntegerField(read_only=True)

    class Meta:
        model = SaleHistorySerializer.Meta.model
        fields = ["photo_card", "seller", "price", "fee"]


class SalePriceUpdateSerializer(SaleHistorySerializer):
    """
    판매 가격 변경 serializer
    """

    fee = serializers.IntegerField(read_only=True)
    renewal_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SaleHistorySerializer.Meta.model
        fields = [
            "price",
            "fee",
            "renewal_date",
        ]


class SaleDetailSerializer(serializers.ModelSerializer):
    """
    판매 내역 serializer
    """

    total_price = serializers.IntegerField(read_only=True)
    sale_history = SaleHistorySerializer(many=True, read_only=True)
    state = serializers.SerializerMethodField()

    class Meta:
        model = SaleHistory
        fields = [
            "id",
            "photo_card_id",
            "price",
            "fee",
            "total_price",
            "state",
            "sale_history",
        ]

    def get_state(self, value):
        return value.get_state_display()
