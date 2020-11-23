from django.db import models
from django.contrib.auth.models import User  

# Create your models here.

# 植物資料
class Plant(models.Model):
    pid=models.AutoField(primary_key=True)
    plant_name=models.CharField(max_length=20)
    active=models.BooleanField()
    create_time=models.DateTimeField(auto_now=True)
    

    @classmethod
    def __str__(self):
        return self.pid
 
# 環境紀錄
class SensorRecord(models.Model):
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    temperature=models.FloatField()
    air=models.FloatField()
    soil=models.FloatField()
    light=models.FloatField()
    create_time=models.DateTimeField(auto_now=True)

    @classmethod
    def __str__(self):
        return 'Temperature %s.</br> Air Humidity %s.</br> Solar Radiation %s.</br> Soil Moisture %s.'% (self.temperature, self.air , self.light, self.soil)

# 日平均環境紀錄
class DailySensorRecord(models.Model):
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    temperature=models.FloatField()
    air=models.FloatField()
    soil=models.FloatField()
    light=models.FloatField()
    create_time=models.DateTimeField(auto_now=True)

    @classmethod
    def __str__(self):
        return 'Temperature %s.</br> Air Humidity %s.</br> Solar Radiation %s.</br> Soil Moisture %s.'% (self.temperature, self.air , self.light, self.soil)

# 月平均環境紀錄
class MonthlySensorRecord(models.Model):
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    temperature=models.FloatField()
    air=models.FloatField()
    soil=models.FloatField()
    light=models.FloatField()
    create_time=models.DateTimeField(auto_now=True)

    @classmethod
    def __str__(self):
        return 'Temperature %s.</br> Air Humidity %s.</br> Solar Radiation %s.</br> Soil Moisture %s.'% (self.temperature, self.air , self.light, self.soil)

# 澆花紀錄
class WaterRecord(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    create_time=models.DateTimeField(auto_now=True)
    create_user=models.IntegerField()

    @classmethod
    def __str__(self):
        return 'Recent watering time is %s.'%(self.create_time)

# 操作紀錄
class OperationRecord(models.Model):
    EVENT_TYPES = (
        ('L', "Light"),
        ('A', "Auto_Watering"),
        ('M', "Manual_Watering"),
        ('N', "New_Plantname"),
        ('R', "Reset_PlantData")
    )

    EVENT_ACTIONS=(
        ('0',"Off"),
        ('1',"On"),
    )

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    event=models.CharField(max_length=1, choices=EVENT_TYPES)
    action=models.CharField(max_length=1, choices=EVENT_ACTIONS)
    create_time=models.DateTimeField(auto_now=True)
    

    @classmethod
    def __str__(self):
        return self.event
# 盆栽狀態
class PotStatus(models.Model):
    light=models.BooleanField(default=0)
    autowater=models.BooleanField(default=0)
    manualwater=models.BooleanField(default=0)

    @classmethod
    def current_pot_status(self):
        return 'Status: Light is %s.</br> Autowatering is %s.</br> Manualwatering is %s.'% (self.light, self.autowater, self.manualwater)

# 評分紀錄
class Scoring(models.Model):

    SCORE_TYPES=(
        ('1', "One"),
        ('2', "Two"),
        ('3', "Three"),
        ('4', "Four"),
        ('5', "Five"),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    score=models.IntegerField(choices=SCORE_TYPES)
    create_time=models.DateTimeField(auto_now=True)

