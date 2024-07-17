from rest_framework import serializers

from .models import SaleHistory


class SaleHistorySerializer(serializers.ModelSerializer):
    """
    판매 내역 serializer
    """

    class Meta:
        model = SaleHistory
        fields = "__all__"
