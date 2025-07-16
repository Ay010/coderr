from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from reviews.models import Review
from reviews.api.serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reviews.api.permissions import IsCustomer, IsCreator
from reviews.api.filters import ReviewFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from datetime import datetime


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['rating', 'updated_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomer()]
        return [IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        if Review.objects.filter(reviewer=request.user, business_user=request.data['business_user']).exists():
            return Response({'error': 'You have already reviewed this business'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['reviewer'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsCreator]

    def update(self, request, *args, **kwargs):
        # Erstelle ein neues Dictionary mit den zu aktualisierenden Daten
        update_data = {}
        if request.data.get('rating') is not None:
            update_data['rating'] = request.data.get('rating')
        if request.data.get('description') is not None:
            update_data['description'] = request.data.get('description')

        # Füge updated_at hinzu
        update_data['updated_at'] = datetime.now()

        # Erstelle eine Kopie des Requests mit den neuen Daten
        request._full_data = update_data

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
