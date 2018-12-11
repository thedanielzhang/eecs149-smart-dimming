from rest_framework import serializers
from app.models import Schedule, Light

class ScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    max_setting = serializers.IntegerField(required=True)
    min_setting = serializers.IntegerField(required=True)
    day_of_week = serializers.CharField(required=False, allow_blank=True, max_length=100)
    hour = serializers.IntegerField(required=True)
    minute = serializers.IntegerField(required=True)
    schedule_id = serializers.CharField(required=False, allow_blank=True, max_length=100)
    light_id = serializers.IntegerField(required=True)
    """
    max_setting = serializers.ListTextField(
        base_field=serializers.IntegerField()
    )
    min_setting = serializers.ListTextField(
        base_field=serializers.IntegerField()
    )
    day_of_week = serializers.ListTextField(
        base_field=serializers.CharField(max_length=10)
    )
    hour = serializers.ListTextField(
        base_field=serializers.IntegerField()
    )
    minute = serializers.ListTextField(
        base_field=serializers.IntegerField()
    )
    """

    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)

        
        instance.max_setting = validated_data.get('max_setting', instance.max_setting)
        instance.min_setting = validated_data.get('min_setting', instance.min_setting)
        instance.day_of_week = validated_data.get('day_of_week', instance.day_of_week)
        instance.hour = validated_data.get('hour', instance.hour)
        instance.minute = validated_data.get('minute', instance.minute)
        instance.schedule_id = validated_data.get('schedule_id', instance.schedule_id)
        instance.light_id = validated_data.get('light_id', instance.light_id)
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
