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
    setting = serializers.DecimalField(max_digits=4, decimal_places=2, default=100)
    scheduleId = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.setting = validated_data.get('setting', instance.setting)
        instance.scheduleId = validated_data.get('scheduleId', instance.scheduleId)

        instance.save()
        return instance
