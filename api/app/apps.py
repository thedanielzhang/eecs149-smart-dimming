from django.apps import AppConfig
import sys
sys.path.append("../")
from bluepy import btle
from crontab import CronTab

devices = None
cron = None

class AppConfig(AppConfig):
    name = 'app'
    print("Connecting...")
    global devices
    devices = {}
    global cron
    cron = CronTab(user='pi')

        
