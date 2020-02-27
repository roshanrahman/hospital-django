# Generated by Django 3.0.2 on 2020-02-24 07:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200217_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='working_on_weekend',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='weekday_availability',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=1), default=[1, 1, 1, 1, 1, 1, 1], size=7),
        ),
    ]
