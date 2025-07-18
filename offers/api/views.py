from rest_framework.generics import ListCreateAPIView
from offers.api.serializers import OfferSerializer, OfferDetailSerializer
from offers.models import Offer, OfferDetail
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user_auth.models import User
from offers.api.permissions import IsBusinessUser, IsCreator
from offers.api.paginations import OfferPagination
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from offers.api.filters import OfferFilter, CustomOrderingFilter
from rest_framework.filters import SearchFilter
import json
from rest_framework import status


class OfferListCreateAPIView(ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, CustomOrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['min_price', 'updated_at']
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        validated_data = request.data
        validated_data['user'] = request.user
        details_data = validated_data.pop('details')
        if len(details_data) != 3:
            raise ValidationError(
                {"details": "3 details required"})
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            offer_detail_serializer = OfferDetailSerializer(data=detail_data)
            features = detail_data.pop('features')
            if offer_detail_serializer.is_valid():
                detail = offer_detail_serializer.save()
                if features:
                    detail.set_features(features)
                    detail.save()
                offer.details.add(detail)
                offer.save()
            else:
                raise ValidationError(offer_detail_serializer.errors)
        return Response(OfferSerializer(offer, context={'request': request}).data, status=status.HTTP_201_CREATED)


class SingleOfferAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsCreator()]
        return [IsAuthenticated()]

    def validate_details(self, details):
        for detail in details:
            if not detail.get('offer_type'):
                raise ValidationError(
                    {"details": "Offer type is required"})
        return details

    def update(self, request, *args, **kwargs):
        if request.data.get('details'):
            details = self.validate_details(request.data.get('details'))

            details_data = request.data.pop('details')
            for detail_data in details_data:
                offer_type = detail_data['offer_type']
                if detail_data.get('features'):
                    features = json.dumps(detail_data.pop('features'))
                    detail_data['features'] = features

                offer = self.get_object()
                detail = offer.details.get(offer_type=offer_type)
                detail_serializer = OfferDetailSerializer(
                    detail, data=detail_data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    raise ValidationError(detail_serializer.errors)
        else:
            raise ValidationError({"details": "Details are required"})

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferDetailDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
