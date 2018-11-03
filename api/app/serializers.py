from rest_framework import serializers
from app.models import Schedule, Light

class ScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class LightSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    lightSetting = serializers.IntegerField(required=False)
    scheduleId = serializers.IntegerField(required=False)

    def create(self, validated_data):
        print("we are in create")
        return Light.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.lightSetting = validated_data.get('lightSetting', instance.lightSetting)
        instance.scheduleId = validated_data.get('scheduleId', instance.scheduleId)

        instance.save()
        return instance
