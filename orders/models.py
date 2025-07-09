from django.db import models
from django.conf import settings
from offers.models import OfferDetail

# Create your models here.


class Order(models.Model):
    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business_orders')
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
