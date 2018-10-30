from django.db import models

# Create your models here.

# Class representing schedule
class Schedule(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    # Activated field?

    class Meta:
        ordering = ('created',)

# Class representing light
class Light(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    setting = models.DecimalField(max_digits=4, decimal_places=2) # This represents the dimness of the light
    scheduleId = models.IntegerField(default=-1) # This links Light to a Schedule - if negative, there is no associated schedule

    class Meta:
        ordering = ('created',)
    