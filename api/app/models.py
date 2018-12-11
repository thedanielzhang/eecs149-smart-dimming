from django.db import models
"""from django_mysql import models as django_models """
# Create your models here.

# Class representing schedule
class Schedule(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    # Activated field?
    max_setting = models.IntegerField(default=0)
    min_setting = models.IntegerField(default=0)
    day_of_week = models.CharField(max_length=100, blank=True, default='')
    hour = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    schedule_id = models.CharField(max_length=100, blank=True, default='')
    light_id = models.IntegerField(default=0)
    """
    max_setting = django_models.ListTextField(
        base_field=models.IntegerField()
    )
    min_setting = django_models.ListTextField(
        base_field=models.IntegerField()
    )
    day_of_week = django_models.ListTextField(
        base_field=models.CharField(max_length=10)
    )
    hour = django_models.ListTextField(
        base_field=models.IntegerField()
    )
    minute = django_models.ListTextField(
        base_field=models.IntegerField()
    )
    """

    class Meta:
        ordering = ('created',)

# Class representing light
class Light(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    scheduleId = models.IntegerField(default=-1) # This links Light to a Schedule - if negative, there is no associated schedule
    lightMAC = models.CharField(max_length=100, blank=True, default='')
    lightSetting = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)
    
