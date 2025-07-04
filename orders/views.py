from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.api.serializers import OrderSerializer
from orders.models import Order
# Create your views here.
