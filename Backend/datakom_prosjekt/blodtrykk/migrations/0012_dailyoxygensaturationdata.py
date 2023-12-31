# Generated by Django 4.2.6 on 2023-11-15 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blodtrykk', '0011_alter_dailybloodpressuredata_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyOxygenSaturationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oxygen_saturation', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_blood_oxygen_saturation_data', to='blodtrykk.patient')),
            ],
        ),
    ]
