# Generated by Django 4.2.5 on 2023-10-24 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API_Handler', '0011_remove_doctor_cnic_users_cnic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='Cnic',
            new_name='cnic',
        ),
    ]
