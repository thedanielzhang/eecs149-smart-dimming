from django.apps import AppConfig
import sys
sys.path.append("../")
from bluepy import btle


devices = None

class AppConfig(AppConfig):
    name = 'app'
    print("Connecting...")
    global devices
    devices = {}

        
