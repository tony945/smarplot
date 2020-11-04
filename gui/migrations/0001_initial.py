# Generated by Django 3.1.2 on 2020-10-29 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_name', models.CharField(max_length=20)),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PotStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('light', models.BooleanField(default=0)),
                ('autowater', models.BooleanField(default=0)),
                ('manualwater', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WaterRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manual', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('create_user', models.IntegerField()),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gui.plant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SensorRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pressure', models.FloatField()),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('light', models.FloatField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gui.plant')),
            ],
        ),
        migrations.CreateModel(
            name='OperationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('L', 'Light'), ('A', 'Auto_Watering'), ('M', 'Manual_Watering')], max_length=1)),
                ('action', models.CharField(choices=[('0', 'Off'), ('1', 'On')], max_length=1)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gui.plant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]