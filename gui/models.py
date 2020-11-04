from django.db import models
from django.contrib.auth.models import User                     
# Create your models here.

# 植物資料
class Plant(models.Model):
    plant_name=models.CharField(max_length=20)
    create_time=models.DateTimeField(auto_now=True)

    @classmethod
    def __str__(self):
        return self.plant_name
 
# 環境變數
class SensorRecord(models.Model):
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    pressure=models.FloatField()
    temperature=models.FloatField()
    humidity=models.FloatField()
    light=models.FloatField()
    create_time=models.DateTimeField(auto_now=True)

    @classmethod
    def __str__(self):
        return self.record_id

# 澆花紀錄
class WaterRecord(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    manual=models.BooleanField(default=0)
    create_time=models.DateTimeField(auto_now=True)
    create_user=models.IntegerField()

    @classmethod
    def __str__(self):
        return self.water_id

# 操作紀錄
class OperationRecord(models.Model):
    EVENT_TYPES = (
        ('L', 'Light'),
        ('A', 'Auto_Watering'),
        ('M', 'Manual_Watering'),
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
        return self.action
# 盆栽狀態
class PotStatus(models.Model):
    light=models.BooleanField(default=0)
    autowater=models.BooleanField(default=0)
    manualwater=models.BooleanField(default=0)

    @classmethod
    def current_pot_status(self):
        return 'Status: Light is %s.</br> Autowatering is %s.</br> Manualwatering is %s.'
