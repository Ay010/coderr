from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles.api.serializers import ProfileDetailSerializer
from profiles.models import Profile
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from user_auth.models import User
from rest_framework.permissions import IsAuthenticated
from profiles.api.permissions import IsProfileOwner


class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileDetailSerializer
    queryset = Profile.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsProfileOwner()]

    def get(self, request, *args, **kwargs):

        response = self.retrieve(request, *args, **kwargs)
        user = User.objects.get(id=response.data['user'])
        response.data['username'] = user.username
        response.data['email'] = user.email
        response.data['type'] = user.type
        return response

    def patch(self, request, *args, **kwargs):
        # Hole das Profil-Objekt
        profile = self.get_object()

        # Erlaubte Felder für das Profil
        allowed_profile_fields = ['first_name', 'last_name',
                                  'location', 'tel', 'description', 'working_hours']

        # Erlaubte Felder für den User
        allowed_user_fields = ['email']

        # Aktualisiere Profil-Felder
        for field in allowed_profile_fields:
            if field in request.data:
                setattr(profile, field, request.data[field])

        # Speichere das Profil
        profile.save()

        # Aktualisiere User-Felder (email)
        user = profile.user
        for field in allowed_user_fields:
            if field in request.data:
                setattr(user, field, request.data[field])

        # Speichere den User
        user.save()

        # Serialisiere und gib die Antwort zurück
        serializer = self.get_serializer(profile)
        response_data = serializer.data
        response_data['username'] = user.username
        response_data['email'] = user.email
        response_data['type'] = user.type

        return Response(response_data, status=status.HTTP_200_OK)


class ListBusinessProfilesView(ListAPIView):
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user__type='business')

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        for profile in response.data:
            user = User.objects.get(id=profile['user'])
            profile['type'] = user.type
            profile['username'] = user.username
        return Response(response.data, status=status.HTTP_200_OK)


class ListCustomerProfilesView(ListAPIView):
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user__type='customer')

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        for profile in response.data:
            user = User.objects.get(id=profile['user'])
            profile['type'] = user.type
            profile['username'] = user.username
        return Response(response.data, status=status.HTTP_200_OK)
