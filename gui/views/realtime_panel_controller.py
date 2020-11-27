from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
from gui.models import Plant, Scoring, PotStatus
from django.contrib.auth.models import User
from datetime import date

# packages for aquiring data from sensor
try:
    import os
    import glob
    import time
    import spidev  # To communicate with SPI devices
    import smbus
    import sys
    import RPi.GPIO as GPIO
    from numpy import interp  # To scale values. Mapping value range of 0~1023 to 0~100
    from time import sleep
    import adafruit_dht
    import board
except:
    print("Module missing for connecting to sensor")

# Global variables for connecting to Sensor



try:
    os.system('pkill libgpiod')
    dhtDevice = adafruit_dht.DHT11(board.D17)



    I2C = smbus.SMBus(1)  # 指定使用/dev/i2c-1

    BASE_DIR = '/sys/bus/w1/devices/'
    DEVICE_FOLDER = glob.glob(BASE_DIR + '28*')[0]
    DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'
except :
    print("Sensor error")


# 實時資訊頁面

@login_required
def realtime_panel(request):
    username = request.session.get("user", '')

    today = date.today()
    formatToday = today.strftime("%Y-%m-%d")

    # Check for status of scoring
    currentPlantID = Plant.objects.get(active=1).pid
    scoreObj = Scoring.objects.filter(plant_id=currentPlantID).filter(create_time=formatToday)

    if scoreObj:
        score = scoreObj[0].score
    else:
        score = "0"
        
    # Check for status of switch
    potstatus = PotStatus.objects.get(id=1)
    lightStatus = potstatus.light
    autowaterStatus = potstatus.autowater
    manualwaterStatus = potstatus.manualwater

    return render(request, "panel/realtime_panel.html", {"user": username, "score": score, "light":lightStatus, "manual":manualwaterStatus, "auto": autowaterStatus})


# 處理評分

@login_required
def scoring(request):
    score = request.POST.get("scoring", '')
    username = request.session.get("user", '')
    user = User.objects.get(username=username)
    plant = Plant.objects.get(active="1")
    
    today = date.today()
    formatToday= today.strftime("%Y-%m-%d")
    # If this plant has yet have any scoring record today, create one
    scoreObj = Scoring.objects.filter(plant_id=plant.pid).filter(create_time=formatToday)
    if scoreObj:
        scoreObj.update(score = score)
    else:
        submitScore = Scoring.objects.create(user=user,plant=plant,score=score,)

    return HttpResponse()


# 自動澆花按鈕行為

@login_required
def autowater(request):
    status = request.POST.get("status", '')
    potstatus = PotStatus.objects.get(id=1)
    potstatus.autowater = status
    potstatus.save()

    return HttpResponse() 


# 光源開關

def light(request):
    status = request.POST.get("status", '')
    potstatus = PotStatus.objects.get(id=1)
    potstatus.light = status
    potstatus.save()

    return HttpResponse()  


# 手動澆花按鈕行為

def manualwater(request):
    status = request.POST.get("status", '')
    potstatus = PotStatus.objects.get(id=1)
    potstatus.manualwater = status
    potstatus.save()

    return HttpResponse() 

# 處理及時資訊更新
# Handler for ajax request

@login_required
def realtime_data_refresh(request):

    # GPIO.BOARD 選項是指定在電路版上接腳的號碼 / GPIO.BCM 選項是指定GPIO後面的號碼
    #GPIO.setmode(GPIO.BOARD)

    # Execute linux command: Add and remove modules from linux kernal : 1-wire bus master driver
    #
    # w1-gpio: GPIO 1-wire bus master driver.
    # The driver uses the GPIO API to control the wire and the GPIO pin can be specified using GPIO machine descriptor tables
    #
    # w1_therm: provides basic temperature conversion for ds18*20 devices, and the ds28ea00 device.
    #os.system('modprobe w1-gpio')
    #os.system('modprobe w1-therm')

    # Aquire data from sensor
    try:
        soilMoisture = readMoist()
    except:
        soilMoisture = "0"
    try:
        light = readLight()
    except:
        light = "0"
    try:
        temp = readTemp()
    except:
        temp = "0"
    try:
        airHumidity = readHumidity()
    except:
        airHumidity = "0"

    # Pack the data into dict, then dump into json
    data = {'light': light, 'temp': temp, 'soil': soilMoisture, 'air': airHumidity}
    data = json.dumps(data)

    return HttpResponse(data)


# Below are the functions used to handle reading from sensor

# Read MCP3008 data
def analogInput(channel):
    # Start SPI connection
    spi = spidev.SpiDev()  # Created an object
    spi.open(0, 0)
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1, (8+channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def readRawTemp():
    f = open(DEVICE_FILE, 'r')
    lines = f.readlines()
    f.close()
    return lines

def readTemp():
    lines = readRawTemp()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readRawTemp()

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0

    return round(temp_c, 1)

def convertToNumber(data):
    return ((data[1] + (256 * data[0])) / 1.2)

def readLight():
    addr=DEVICE_ADDRESS
    data = I2C.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_2)
    return round(convertToNumber(data), 1)

def readMoist():
    data = analogInput(0)  # Reading from CH0
    data = interp(data, [0, 1023], [100, 0])
    return int(data)

def readHumidity():
    data = dhtDevice.humidity
    return data

