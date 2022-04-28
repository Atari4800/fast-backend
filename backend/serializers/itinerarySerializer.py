from rest_framework import serializers
from backend.models import Client


class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ["location", "languages"]
