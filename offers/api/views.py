from rest_framework.generics import ListCreateAPIView
from offers.api.serializers import OfferSerializer, OfferDetailSerializer
from offers.models import Offer, OfferDetail
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView
from offers.models import Offer
from offers.api.serializers import OfferSerializer, OfferDetailSerializer
from user_auth.models import User
from offers.api.permissions import IsBusinessUser
from offers.api.paginations import OfferPagination
from rest_framework.generics import RetrieveAPIView


class OfferListCreateAPIView(ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):

        validated_data = request.data
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
        return Response(OfferSerializer(offer).data)


class OfferDetailDetailAPIView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer

    def get_object(self):
        return self.queryset.get(id=self.kwargs['id'])
