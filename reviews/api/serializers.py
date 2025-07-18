from rest_framework import serializers
from reviews.models import Review
from datetime import datetime


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']

    def validate_business_user(self, value):
        business_user = value
        if business_user.type != 'business':
            raise serializers.ValidationError(
                "business_user must be type business")
        return business_user
