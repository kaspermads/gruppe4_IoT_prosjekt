# Generated by Django 4.2.6 on 2023-11-09 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blodtrykk', '0010_dailybloodpressuredata_oxygen_saturation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailybloodpressuredata',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_blood_pressure_data', to='blodtrykk.patient'),
        ),
    ]
