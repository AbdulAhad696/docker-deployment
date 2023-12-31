# Generated by Django 4.1.3 on 2023-08-13 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Domain', models.CharField(max_length=20)),
                ('Experience', models.SmallIntegerField()),
                ('Bio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Lookup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Type', models.TextField()),
                ('Value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('MedName', models.CharField(max_length=255)),
                ('Dosage', models.CharField(max_length=255)),
                ('Current', models.BooleanField()),
                ('PrescribedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=30)),
                ('usertype', models.SmallIntegerField()),
                ('contact', models.CharField(blank=True, max_length=11, null=True)),
                ('Fname', models.CharField(max_length=15)),
                ('Lname', models.CharField(max_length=15)),
                ('Gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.lookup')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Age', models.SmallIntegerField()),
                ('BloodGroup', models.CharField(max_length=2)),
                ('Weight', models.SmallIntegerField()),
                ('Height', models.CharField(max_length=5)),
                ('DoB', models.DateField()),
                ('BMI', models.FloatField()),
                ('AdmitSysBP', models.SmallIntegerField()),
                ('AdmitDiBP', models.SmallIntegerField()),
                ('AdmitBPM', models.SmallIntegerField()),
                ('AdmitTemp', models.SmallIntegerField()),
                ('AdmitO2', models.SmallIntegerField()),
                ('NursingDiagnosis', models.TextField()),
                ('MedicalDiagnosis', models.TextField()),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.users')),
                ('Ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.ward')),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Type', models.SmallIntegerField()),
                ('Experience', models.SmallIntegerField()),
                ('Bio', models.CharField(max_length=50)),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.users')),
                ('Ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.ward')),
            ],
        ),
        migrations.CreateModel(
            name='MedicationSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateAdministered', models.DateField()),
                ('TimeAdministered', models.TimeField()),
                ('AdministeredBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.nurse')),
                ('MedId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.medication')),
            ],
        ),
        migrations.AddField(
            model_name='medication',
            name='PrescribedTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.patient'),
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('Date', models.DateField()),
                ('Link', models.CharField(max_length=255)),
                ('PatientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.patient')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='UserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.users'),
        ),
        migrations.CreateModel(
            name='CareVitals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.TimeField()),
                ('Date', models.DateField()),
                ('SystolicBP', models.SmallIntegerField()),
                ('DistolicBP', models.SmallIntegerField()),
                ('HeartRate', models.SmallIntegerField()),
                ('Temperature', models.FloatField()),
                ('SpO2', models.SmallIntegerField()),
                ('RespirationRate', models.SmallIntegerField()),
                ('PatientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Handler.patient')),
            ],
        ),
    ]
