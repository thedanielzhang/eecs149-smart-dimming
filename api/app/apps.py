from django.apps import AppConfig
import sys
sys.path.append("../")
from bluepy import btle
from app.models import Light

devices = None

class AppConfig(AppConfig):
    name = 'app'
    print("Connecting...")
    def ready(self):
        global devices
        devices = []

        
