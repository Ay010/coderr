from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user_auth.api.serializers import RegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from user_auth.models import User
from django.contrib.auth import authenticate
from profiles.models import Profile
from profiles.api.serializers import ProfileDetailSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            serializer.data['token'] = token.key

            profile_data = {'user': user.id}
            profile_serializer = ProfileDetailSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                print("Profile Serializer Fehler:", profile_serializer.errors)

            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):

        if 'username' not in request.data or 'password' not in request.data or not request.data['username'] or not request.data['password']:
            return Response({
                "error": "username and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(
                username=request.data['username'], password=request.data['password'])

        if user:
            serializer = UserSerializer(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_200_OK)
        return Response({
            "error": "Invalid credentials"
        }, status=status.HTTP_400_BAD_REQUEST)
