from django.db import models
from user_auth.models import User

# Create your models here.


class Review(models.Model):
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviewer_reviews')
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
