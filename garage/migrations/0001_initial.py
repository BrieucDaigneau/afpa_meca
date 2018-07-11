# Generated by Django 2.0.5 on 2018-07-09 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle_modele', models.CharField(max_length=50, verbose_name='libellé modele')),
            ],
        ),
        migrations.CreateModel(
            name='Motorise',
            fields=[
                ('vehicule_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='garage.Vehicule')),
                ('libelle_marque', models.CharField(max_length=100, verbose_name='libellé marque')),
            ],
            bases=('garage.vehicule',),
        ),
    ]
