from django.apps import AppConfig
import sys
sys.path.append("../")
from bluepy import btle

class AppConfig(AppConfig):
    name = 'app'
    print("Connecting...")
    device = btle.Peripheral("MAC:ADDRESS:1")
