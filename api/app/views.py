from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from app.models import Schedule, Light
from app.serializers import ScheduleSerializer, LightSerializer, ScanSerializer, EventSerializer
from rest_framework.response import Response
from rest_framework import status
from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
from app.apps import devices
from app.apps import cron
import struct
import sqlite3
from django.conf import settings
import os

light_db = os.path.join(settings.BASE_DIR, 'lights.db')

# Create your views here.
@api_view(['GET'])
def dashboard(request):
    id = int(request.GET.get('id', 0))
    mac = request.GET.get('mac')
    conn = sqlite3.connect(light_db)
    c = conn.cursor()
    configured_lights = []
    for (name, id, connected) in c.execute("SELECT name, id, connected FROM lights WHERE name IS NOT NULL ORDER BY id ASC"):
        configured_lights.append({'name':name,'id':id,'connected':connected==1})
    unconfigured_lights = []
    for (mac, connected) in c.execute("SELECT mac, connected FROM lights WHERE name IS NULL"):
        unconfigured_lights.append({'mac':mac,'connected':connected==1})
    c.execute("SELECT char_value, connected, name FROM lights WHERE id = ? AND char_value IS NOT NULL", (id,))
    current_light = {}
    entry = c.fetchone()
    char_value = entry[0]
    if entry and not mac:
        current_light['light_level'] = 255 - (char_value & 0xFF)
        current_light['source'] = (char_value >> 8) & 0x7
        current_light['light_tracking'] = ((char_value >> 11) & 1) == 1
        current_light['motion_tracking'] = ((char_value >> 12) & 1) == 1
        current_light['connected'] = entry[1] == 1
    return render(request, 'dashboard/index.html', {'configured':configured_lights, 'unconfigured':unconfigured_lights, 'current_light': current_light, 'mac':mac})

@api_view(['POST'])
def configure_light(request):
    conn = sqlite3.connect(light_db)
    c = conn.cursor()
    c.execute("UPDATE lights SET name = ?1, id = ?2 WHERE mac = ?3", (request.data['name'], request.data['id'], request.data['mac']))
    conn.commit()
    return HttpResponse(status=201)

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
        serialized_data['lightSetting'] = struct.unpack("I", bytearray(devices[pk].getCharacteristics(uuid="0000beef-1212-efde-1523-785fef13d123")[0].read()))
        """serialized_data['lightSetting'] = bytearray(devices[pk].getCharacteristics(uuid="0000beef-1212-efde-1523-785fef13d123")[0].read())"""
        print(list(devices[pk].getCharacteristics(uuid="0000beef-1212-efde-1523-785fef13d123")[0].read()))
        return Response(serialized_data)
    elif request.method == 'PUT':
        serializer = LightSerializer(light, data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data['lightSetting'])
            data_as_bytes = serializer.validated_data['lightSetting'].to_bytes(4, byteorder='little')
            print(data_as_bytes)
            devices[pk].getCharacteristics(uuid="0000beef-1212-efde-1523-785fef13d123")[0].write(data_as_bytes)
            serializer.save()
            return Response(serializer.validated_data)
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
    """ pk is light_id """
    
    if request.method == 'GET':
        for job in cron:
            print(job)
        schedulesModels = Schedule.objects.filter(light_id=pk)
        scheduleSerializer = ScheduleSerializer(schedulesModels, many=True)
        events = []
        schedules = scheduleSerializer.data
        for i in range(0, len(schedules), 2):
            event = {}
            print(schedules[i])
            event['schedule_id'] = schedules[i].get('schedule_id')
            event['text'] = "Min: " + str(schedules[i].get('min_setting')) + "%\nMax: " + str(schedules[i].get('max_setting')) + "%"
            start_date = ""
            if schedules[i].get('day_of_week') == "MON":
                start_date = "12/29/1969 "
            elif schedules[i].get('day_of_week') == "TUE":
                start_date = "12/30/1969 "
            elif schedules[i].get('day_of_week') == "WED":
                start_date = "12/31/1969 "
            elif schedules[i].get('day_of_week') == "THU":
                start_date = "1/1/1970 "
            elif schedules[i].get('day_of_week') == "FRI":
                start_date = "1/2/1970 "
            elif schedules[i].get('day_of_week') == "SAT":
                start_date = "1/3/1970 "
            elif schedules[i].get('day_of_week') == "SUN":
                start_date = "1/4/1970 "
            event['start_date'] = start_date + str(schedules[i].get('hour')) + ":" + str(schedules[i].get('minute'))


            end_date = ""
            if schedules[i+1].get('day_of_week') == "MON":
                end_date = "12/29/1969 "
            elif schedules[i+1].get('day_of_week') == "TUE":
                end_date = "12/30/1969 "
            elif schedules[i+1].get('day_of_week') == "WED":
                end_date = "12/31/1969 "
            elif schedules[i+1].get('day_of_week') == "THU":
                end_date = "1/1/1970 "
            elif schedules[i+1].get('day_of_week') == "FRI":
                end_date = "1/2/1970 "
            elif schedules[i+1].get('day_of_week') == "SAT":
                end_date = "1/3/1970 "
            elif schedules[i+1].get('day_of_week') == "SUN":
                end_date = "1/4/1970 "
            event['end_date'] = end_date + str(schedules[i+1].get('hour')) + ":" + str(schedules[i+1].get('minute'))

            events.append(event)
        eventSerializer = EventSerializer(events, many=True)
        return JsonResponse(eventSerializer.data, safe=False)
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

    serializer = ScanSerializer(scanned_devices, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def create_schedule(request, pk):
    """ pk is light id """

    print("We are in create_schedule")
    print(request)
    data = JSONParser().parse(request)
    print("We are in create_schedule")
    serializer = ScheduleSerializer(data=data, many=True)
    
    if serializer.is_valid():
        

        print(serializer.data)
        for event in serializer.data:
            
            job = cron.new(command='python3 /home/pi/eecs149-smart-dimming/write_schedule.py --id=%d --min=%d --max=%d' % (event.get('light_id'), data.get('min_setting'), data.get('max_setting')), comment=event.get('schedule_id'))
            job.dow.on(event.get('day_of_week'))
            
            job.hour.on(event.get('hour'))
            job.minute.on(event.get('minute'))
            cron.write()
        serializer.save()
        return JsonResponse(serializer.data, status=201, safe=False)
    return JsonResponse(serializer.errors, status=400, safe=False)

@csrf_exempt
@api_view(['DELETE'])
def delete_schedule(request, pk):
    # pk is the schedule id
    schedules = Schedule.objects.filter(schedule_id=pk).delete()
    cron.remove_all(comment=pk)
    return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET'])
def connect(request):
    # Connect to saved lights
    connected_lights = []
    for light in Light.objects.all():
        if len(light.lightMAC) > 0:
            try:
                device = btle.Peripheral(light.lightMAC, btle.ADDR_TYPE_RANDOM)
                print(device.getCharacteristics(uuid="0000BEEF1212EFDE1523785FEF13D123"))

                devices[light.id] = device
                connected_lights.append(light)
            except:
                print(light.name + " already connected, or can't connect")

    serializer = LightSerializer(connected_lights, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def connect_specific(request, pk):
    try:
        light = Light.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return HttpResponse(status=404)
    if len(light.lightMAC) > 0:
        try:
            device = btle.Peripheral(light.lightMAC, btle.ADDR_TYPE_RANDOM)
            print(device.getCharacteristics(uuid="0000BEEF1212EFDE1523785FEF13D123"))

            devices[light.id] = device
        except:
            print(light.name + " already connected, or can't connect")
    serializer = LightSerializer(light)
    return Response(serializer.data)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)
