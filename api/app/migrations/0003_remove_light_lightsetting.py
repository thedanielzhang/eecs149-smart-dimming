# Generated by Django 2.1.3 on 2018-12-04 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_light_lightmac'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='light',
            name='lightSetting',
        ),
    ]
