# Generated by Django 4.2.5 on 2023-10-24 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Handler', '0010_users_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='Cnic',
        ),
        migrations.AddField(
            model_name='users',
            name='Cnic',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
