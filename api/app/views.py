from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from app.models import Schedule, Light
from app.serializers import ScheduleSerializer, LightSerializer, ScanSerializer
from rest_framework.response import Response
from rest_framework import status
from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
from app.apps import devices
# Create your views here.

@csrf_exempt
@api_view(['GET', 'POST'])
def light_general(request):
    # GET all and POST methods

    if request.method == 'GET':
        lights = Light.objects.all()
        serializer = LightSerializer(lights, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print("are we here in light_general")
        serializer = LightSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt 
@api_view(['GET', 'PUT', 'DELETE'])
def light_specific(request, pk):
    # GET, UPDATE, and DELETE specific light

    try:
        light = Light.objects.get(pk=pk)
    except Light.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LightSerializer(light)
        serialized_data = serializer.data
        serialized_data['lightSetting'] = 75
        return Response(serialized_data)
    elif request.method == 'PUT':
        serializer = LightSerializer(light, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        light.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def schedule_general(request):
    # GET all and POST methods

    if request.method == 'GET':
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt 
@api_view(['GET', 'PUT', 'DELETE'])
def schedule_specific(request, pk):
    # GET, UPDATE, and DELETE specific light

    try:
        schedule = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ScheduleSerializer(schedule)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ScheduleSerializer(schedule, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        schedule.delete()
        return HttpResponse(status=204)

@csrf_exempt
@api_view(['GET'])
def scan(request):
    # Get all scanned items
    scanner = Scanner().withDelegate(ScanDelegate())
    scanned_devices = scanner.scan(10.0)

    for dev in scanned_devices:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))

    serializer = ScanSerializer(devices, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def connect(request):
    # Connect to saved lights
    connected_lights = []
    for light in Light.objects.all():
        if len(light.lightMAC) > 0:
            try:
                device = btle.Peripheral(light.lightMAC, btle.ADDR_TYPE_RANDOM)
                print(device.getServices())

                devices[light.id].append(device)
                connected_lights.append(light)
            except:
                print(light.name + " already connected, or can't connect")
    
    serializer = LightSerializer(connected_lights, many=True)
    return Response(serializer.data)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)
