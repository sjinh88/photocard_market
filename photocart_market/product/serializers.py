from rest_framework import serializers

from .models import PhotoCard


class PhotoCardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoCard
        fields = ["id", "name", "photo_card", "description"]