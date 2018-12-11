# Generated by Django 2.1.4 on 2018-12-11 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_schedule_light_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_id', models.CharField(blank=True, default='', max_length=100)),
                ('text', models.CharField(blank=True, default='', max_length=100)),
                ('start_date', models.CharField(blank=True, default='', max_length=100)),
                ('end_date', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'ordering': ('schedule_id',),
            },
        ),
    ]
