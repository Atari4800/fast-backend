from rest_framework import serializers
from backend.models import Route


class RouteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):

        route = Route.objects.create(**validated_data)

        route.save()

        return route

    class Meta:
        model = Route
        fields = [
            "id",
            "assigned_to",
            "created_on",
            "total_quantity",
            "total_distance",
            "total_duration",
            "route_list",
            "itinerary",
        ]
