# Generated by Django 2.1.3 on 2018-12-04 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='light',
            name='lightMAC',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]