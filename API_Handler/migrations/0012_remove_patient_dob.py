# Generated by Django 4.1.3 on 2023-11-07 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API_Handler', '0011_rename_age_patient_age_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='DoB',
        ),
    ]