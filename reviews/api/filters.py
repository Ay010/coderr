from django_filters import rest_framework as filters
from reviews.models import Review


class ReviewFilter(filters.FilterSet):
    business_user_id = filters.CharFilter(
        field_name="business_user__id", lookup_expr='in')
    reviewer_id = filters.CharFilter(
        field_name="reviewer__id", lookup_expr='in')

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']
