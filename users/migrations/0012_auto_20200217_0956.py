# Generated by Django 3.0.2 on 2020-02-17 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200217_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('admin', 'Admin')], max_length=30, verbose_name='User type'),
        ),
    ]
