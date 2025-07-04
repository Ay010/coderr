from rest_framework import serializers
from user_auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime
from time import time, ctime
from contextlib import suppress
import warnings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'type',
                  'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        possible_Types = ['customer', 'business']
        if self.validated_data['type'] not in possible_Types:
            raise serializers.ValidationError(
                {'type': 'Invalid type'})

        if self.validated_data['password'] != self.validated_data['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})

        user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            type=self.validated_data['type'],
            password=self.validated_data['password'],
        )
        user.save()
        return user
