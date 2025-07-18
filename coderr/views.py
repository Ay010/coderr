from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from offers.models import Offer
from orders.models import Order
from reviews.models import Review
from profiles.models import Profile
from django.db.models import Avg

# Create your views here.


class BaseInfoView(APIView):
    def get(self, request):
        avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']
        # Begrenze die Dezimalstellen auf 2
        if avg_rating is not None:
            avg_rating = round(avg_rating, 2)

        data = {
            "review_count": Review.objects.count(),
            "average_rating": avg_rating,
            "business_profile_count": Profile.objects.filter(
                user__type='business').count(),
            "offer_count": Offer.objects.count(),
        }
        return Response(data)
