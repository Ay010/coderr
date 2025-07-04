from django.db import models
import json

# Create your models here.


class Offer(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    details = models.ManyToManyField(
        'OfferDetail', related_name='offers')


class OfferDetail(models.Model):
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    features = models.TextField(default='[]')  # JSON-String für Features
    offer_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_features(self):
        data = self.features.split(",")  # convert string to list
        return data

    def set_features(self, features):
        self.features = json.dumps(features)

    def __str__(self):
        return self.title
