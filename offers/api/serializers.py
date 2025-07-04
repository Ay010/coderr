from rest_framework import serializers
from offers.models import Offer, OfferDetail
from datetime import datetime
import json


class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S', read_only=True)
    features = serializers.ListField(required=False, default=list)

    class Meta:
        model = OfferDetail
        fields = ['id', 'url', 'title', 'revisions', 'delivery_time_in_days', 'price',
                  'features', 'offer_type', 'created_at', 'updated_at']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

    def get_fields(self):
        fields = super().get_fields()
        if hasattr(self, 'context') and 'request' in self.context and self.context['request'].method == 'GET':
            # Für GET-Requests nur id und url zurückgeben
            return {key: fields[key] for key in ['id', 'url'] if key in fields}
        else:
            # Für andere Requests alle Felder außer url zurückgeben
            return {key: fields[key] for key in fields if key != 'url'}

    def update(self, instance, validated_data):
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        validated_data['updated_at'] = updated_at

        return super().update(instance, validated_data)

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

        # Prüfe, ob wir in einem GET-Request sind und nur id/url anzeigen sollen
        is_get_request = (hasattr(self, 'context') and
                          'request' in self.context and
                          self.context['request'].method == 'GET')

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

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
