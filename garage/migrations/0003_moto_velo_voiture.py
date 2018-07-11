# Generated by Django 2.0.5 on 2018-07-11 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0002_auto_20180711_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moto',
            fields=[
                ('motorise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='garage.Motorise')),
            ],
            bases=('garage.motorise',),
        ),
        migrations.CreateModel(
            name='Velo',
            fields=[
                ('vehicule_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='garage.Vehicule')),
            ],
            bases=('garage.vehicule',),
        ),
        migrations.CreateModel(
            name='Voiture',
            fields=[
                ('motorise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='garage.Motorise')),
            ],
            bases=('garage.motorise',),
        ),
    ]
