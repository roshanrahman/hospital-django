# Generated by Django 3.0.2 on 2020-02-10 10:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0005_auto_20200204_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='doctors',
            field=models.ManyToManyField(blank=True, limit_choices_to={'specialization__in': models.ManyToManyField(blank=True, to='specializations.Specialization'), 'user_type': 'doctor'}, related_name='doctors', to=settings.AUTH_USER_MODEL),
        ),
    ]
