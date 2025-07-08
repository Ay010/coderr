from django.db import models
import json
from django.conf import settings
# Create your models here.


class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    details = models.ManyToManyField(
        'OfferDetail', related_name='offers')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    min_price = models.IntegerField(default=0)
    min_delivery_time = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Update min_price and min_delivery_time before saving
        if self.pk:  # Only for existing objects
            min_price = self.details.aggregate(
                min_price=models.Min('price'))['min_price']
            min_delivery_time = self.details.aggregate(
                min_delivery_time=models.Min('delivery_time_in_days'))['min_delivery_time']

            if min_price is not None:
                self.min_price = min_price
            if min_delivery_time is not None:
                self.min_delivery_time = min_delivery_time

        super().save(*args, **kwargs)

    def update_min_values(self):
        """Update min_price and min_delivery_time based on current details"""
        min_price = self.details.aggregate(
            min_price=models.Min('price'))['min_price']
        min_delivery_time = self.details.aggregate(
            min_delivery_time=models.Min('delivery_time_in_days'))['min_delivery_time']

        if min_price is not None:
            self.min_price = min_price
        if min_delivery_time is not None:
            self.min_delivery_time = min_delivery_time

        self.save(update_fields=['min_price', 'min_delivery_time'])


class OfferDetail(models.Model):
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    features = models.TextField(default='[]')  # JSON-String für Features
    offer_type = models.CharField(max_length=255)

    def get_features(self):
        data = self.features.split(",")  # convert string to list
        return data

    def set_features(self, features):
        self.features = json.dumps(features)

    def __str__(self):
        return self.title
