from rest_framework import serializers
from backend.models.savings import Savings
from backend.serializers.locationSerializer import LocationSerializer

class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields = ['saving_id', 'origin', 'location1', 'location2', 'saving']

    savings_id = serializers.IntegerField()
    origin = LocationSerializer()
    location1 = LocationSerializer()
    location2 = LocationSerializer()
    savings = serializers.IntegerField()

    def create(self, validated_data):
        return Savings.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.savings_id = validated_data.get('savings_id', instance.savings_id)
        instance.savings = validated_data.get('savings', instance.savings)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.location1 = validated_data.get('location1', instance.location1)
        instance.location2 = validated_data.get('location2', instance.location2)      
        
        instance.save()
        return instance
