from rest_framework import serializers

import money as money_constants
from money.models import (
    Actual,
    Projected,
)

class TransactionSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    category = serializers.SerializerMethodField()
    amount = serializers.FloatField()
    description = serializers.CharField()
    tags = serializers.SerializerMethodField()

    def get_category(self, obj):
        return money_constants.CATEGORY_TO_NAME.get(obj.category)

    def get_tags(self, obj):
        return []


class ActualSerializer(TransactionSerializer):

    def create(self, validated_data):
        return Actual.objects.create(**validated_data)


class ProjectedSerializer(TransactionSerializer):

    def create(self, validated_data):
        return Projected.objects.create(**validated_data)