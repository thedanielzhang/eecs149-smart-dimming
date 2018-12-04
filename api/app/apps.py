from django.apps import AppConfig
import sys
sys.path.append("../")
from bluepy import btle
from app.models import Light

device = None

class AppConfig(AppConfig):
    name = 'app'
    print("Connecting...")
    def ready(self):
        global devices
        devices = []

        for light in Lights.objects.all():
            if len(light.lightMAC) > 0:
                device = btle.Peripheral(light.lightMAC, btle.ADDR_TYPE_RANDOM)
                print(device.getServices())

                devices.append(device)
