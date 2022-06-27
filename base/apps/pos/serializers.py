from rest_framework import serializers
from .models import CashControl
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CashControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashControl
        fields = "__all__"
