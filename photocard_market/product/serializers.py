import django_filters.rest_framework as filters
from rest_framework import serializers

from .models import PhotoCard


class PhotoCardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoCard
        fields = ["id", "name", "photo_card", "description"]


class PhotoCardFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = PhotoCard
        fields = ["name"]
