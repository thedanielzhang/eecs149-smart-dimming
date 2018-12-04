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
    scheduleId = serializers.IntegerField(required=False)
    lightMAC = serializers.CharField(max_length=100, allow_blank=True, default='')


    def create(self, validated_data):
        print("we are in create")
        return Light.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.lightSetting = validated_data.get('lightSetting', instance.lightSetting)
        instance.scheduleId = validated_data.get('scheduleId', instance.scheduleId)
        instance.lightMAC = validated_data.get('lightMAC', instance.lightMAC)
        instance.save()
        return instance

class ScanSerializer(serializers.Serializer):
    addr = serializers.CharField(required=False, allow_blank=True, max_length=100)
    addrType = serializers.CharField(required=False, allow_blank=True, max_length=100)
    rssi = serializers.CharField(required=False, allow_blank=True, max_length=100)
