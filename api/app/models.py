from django.db import models

# Create your models here.

# Class representing schedule
class Schedule(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    # Activated field?
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

    class Meta:
        ordering = ('created',)

# Class representing light
class Light(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    scheduleId = models.IntegerField(default=-1) # This links Light to a Schedule - if negative, there is no associated schedule
    lightMAC = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)
    
