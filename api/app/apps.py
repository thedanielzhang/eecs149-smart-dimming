from django.apps import AppConfig
import sys
sys.path.append("../")
from bluepy import btle

device = None

class AppConfig(AppConfig):
    name = 'app'
    print("Connecting...")
    global device 
    device = btle.Peripheral("D3:45:72:1D:0C:05", btle.ADDR_TYPE_RANDOM)
    print(device.getServices())
