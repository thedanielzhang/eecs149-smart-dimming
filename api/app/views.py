from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from app.models import Schedule, Light
from app.serializers import ScheduleSerializer, LightSerializer

# Create your views here.

@csrf_exempt
def light_general(request):
    # GET all and POST methods

    if request.method == 'GET':
        lights = Light.objects.all()
        serializer = LightSerializer(lights, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LightSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt 
def light_specific(request, pk):
    # GET, UPDATE, and DELETE specific light

    try:
        light = Light.objects.get(pk=pk)
    except Light.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LightSerialier(light)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LightSerialier(light, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        light.delete()
        return HttpResponse(status=204)


@csrf_exempt
def schedule_general(request):
    # GET all and POST methods

    if request.method == 'GET':
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(lights, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt 
def schedule_specific(request, pk):
    # GET, UPDATE, and DELETE specific light

    try:
        schedule = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ScheduleSerializer(light)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ScheduleSerializer(light, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        schedule.delete()
        return HttpResponse(status=204)