from rest_framework import serializers

from backend.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]
        read_only_fields = ["created_on"]

