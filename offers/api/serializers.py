from rest_framework import serializers
from offers.models import Offer, OfferDetail
from datetime import datetime
import json
from django.db.models import Min
from django.urls import reverse


class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url', 'title', 'revisions', 'delivery_time_in_days', 'price',
                  'features', 'offer_type']

    def validate_offer_type(self, value):
        if value not in ['standard', 'premium', 'exclusive']:
            raise serializers.ValidationError(
                "Invalid offer type. Must be 'standard', 'premium', or 'exclusive'.")
        return value

    def get_url(self, obj):
        request = self.context.get('request')

        if request:
            if request.path.startswith('/api/offers/' + str(obj.offers.all().first().id) + '/'):
                return request.build_absolute_uri(reverse('offer-detail-detail', kwargs={'pk': obj.id}))
            else:
                return f"/offerdetails/{obj.id}/"
        else:
            return f"/offerdetails/{obj.id}/"

    def get_fields(self):
        fields = super().get_fields()
        if (hasattr(self, 'context') and 'request' in self.context and
            self.context['request'].method == 'GET' and
                self.context['request'].path.startswith('/api/offers/')):
            # Für GET-Requests auf /api/offers/ nur id und url zurückgeben
            return {key: fields[key] for key in ['id', 'url'] if key in fields}
        else:
            # Für andere Requests alle Felder außer url zurückgeben
            return {key: fields[key] for key in fields if key != 'url'}

    def create(self, validated_data):
        # Features verarbeiten, falls vorhanden
        features = validated_data.pop('features', [])
        instance = super().create(validated_data)
        if features:
            instance.set_features(features)
            instance.save()
        return instance

    def to_representation(self, instance):
        """Konvertiert das Model zurück zu JSON für die API-Ausgabe"""
        data = super().to_representation(instance)

        # Prüfe, ob wir in einem GET-Request auf /api/offers/ sind und nur id/url anzeigen sollen
        is_get_request = (hasattr(self, 'context') and
                          'request' in self.context and
                          self.context['request'].method == 'GET' and
                          self.context['request'].path.startswith('/api/offers/'))

        # Features nur hinzufügen, wenn es kein GET-Request ist oder features in den Feldern enthalten ist
        if not is_get_request or 'features' in data:
            if instance.features:
                try:
                    data['features'] = json.loads(instance.features)
                except json.JSONDecodeError:
                    data['features'] = []
            else:
                data['features'] = []

        return data


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(
        required=False, default=datetime.now)
    updated_at = serializers.DateTimeField(
        required=False, default=datetime.now)
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',
                  'details', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user_details']

    def validate_details(self, details):
        for detail in details:
            if not detail.get('offer_type'):
                raise serializers.ValidationError(
                    {"details": "Offer type is required"})
        return details

    def get_fields(self):
        fields = super().get_fields()
        if (hasattr(self, 'context') and 'request' in self.context and
                self.context['request'].method == 'POST'):
            # Bei POST-Requests nur bestimmte Felder zurückgeben
            allowed_fields = ['id', 'title', 'image', 'description', 'details']
            return {key: fields[key] for key in allowed_fields if key in fields}
        else:
            return fields

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery_time=Min('delivery_time_in_days'))['min_delivery_time']

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }

    def update(self, instance, validated_data):
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        validated_data['updated_at'] = updated_at

        return super().update(instance, validated_data)
