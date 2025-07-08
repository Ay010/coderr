from rest_framework import serializers
from profiles.models import Profile
import warnings
from datetime import datetime
from contextlib import suppress

warnings.filterwarnings("ignore", category=RuntimeWarning,
                        message=".*received a naive datetime.*")


class ProfileDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        required=False, default=datetime.now)

    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'created_at']

    def save(self, **kwargs):

        with suppress(RuntimeWarning):
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        profile = Profile.objects.create(
            user=self.validated_data['user'],
            created_at=created_at
        )
        profile.save()
        return profile
