from rest_framework import generics
from django_filters import rest_framework as filters
from django.db.models import Min
from offers.models import Offer
from offers.api.serializers import OfferSerializer
from rest_framework.filters import OrderingFilter


class OfferFilter(filters.FilterSet):
    min_price = filters.NumberFilter(method='filter_min_price')
    min_delivery_time = filters.NumberFilter(
        method='filter_min_delivery_time')
    creator_id = filters.CharFilter(
        field_name="user__id", lookup_expr='in')

    class Meta:
        model = Offer
        fields = ['min_price', 'creator_id']

    def filter_min_price(self, queryset, name, value):
        """
        Filter offers based on the minimum price from offer details
        """
        return queryset.annotate(
            calculated_min_price=Min('details__price')
        ).filter(calculated_min_price__gte=value)

    def filter_min_delivery_time(self, queryset, name, value):
        """
        Filter offers based on the minimum delivery time from offer details
        """
        return queryset.annotate(
            calculated_min_delivery_time=Min('details__delivery_time_in_days')
        ).filter(calculated_min_delivery_time__gte=value)


class CustomOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)

        if ordering:
            # Replace min_price with the calculated field
            ordering = [field.replace(
                'min_price', 'calculated_min_price') for field in ordering]

        return ordering

    def filter_queryset(self, request, queryset, view):
        # Annotate the queryset with calculated min_price
        queryset = queryset.annotate(
            calculated_min_price=Min('details__price')
        )

        return super().filter_queryset(request, queryset, view)
