from rest_framework import serializers
from app.models import Schedule, Light

class ScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    max_setting = models.ListTextField(
        base_field=IntegerField()
    )
    min_setting = models.ListTextField(
        base_field=IntegerField()
    )
    day_of_week = models.ListTextField(
        base_field=CharField(max_length=10)
    )
    hour = models.ListTextField(
        base_field=IntegerField()
    )
    minute = models.ListTextField(
        base_field=IntegerField()
    )

    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.max_setting = validated_data.get('max_setting', instance.max_setting)
        instance.min_setting = validated_data.get('min_setting', instance.min_setting)
        instance.day_of_week = validated_data.get('day_of_week', instance.day_of_week)
        instance.hour = validated_data.get('hour', instance.hour)
        instance.minute = validated_data.get('minute', instance.minute)
        instance.save()
        return instance


class LightSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    scheduleId = serializers.IntegerField(required=False)
    lightMAC = serializers.CharField(max_length=100, allow_blank=True, default='')
    lightSetting = serializers.IntegerField(required=False)

    def create(self, validated_data):
        print("we are in create")
        return Light.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.scheduleId = validated_data.get('scheduleId', instance.scheduleId)
        instance.lightMAC = validated_data.get('lightMAC', instance.lightMAC)
        instance.save()
        return instance

class ScanSerializer(serializers.Serializer):
    addr = serializers.CharField(required=False, allow_blank=True, max_length=100)
    addrType = serializers.CharField(required=False, allow_blank=True, max_length=100)
    rssi = serializers.CharField(required=False, allow_blank=True, max_length=100)
