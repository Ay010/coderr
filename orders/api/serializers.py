from rest_framework import serializers
from orders.models import Order
from datetime import datetime


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
