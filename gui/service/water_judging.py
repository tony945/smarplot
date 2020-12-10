
#!/usr/bin/python3
# Importing modules
import os
import glob
import time
import spidev  # To communicate with SPI devices
import smbus
import time
import sys
import mariadb
import os
import RPi.GPIO as GPIO
from time import strftime
from datetime import datetime
from numpy import interp  # To scale values
from time import sleep
from joblib import load

import board
import adafruit_dht
os.system('pkill libgpiod')
dhtDevice = adafruit_dht.DHT11(board.D17)

# GPIO.setmode(GPIO.BOARD)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir+'28*')[0]
device_file = device_folder + '/w1_slave'

# Start SPI connection
spi = spidev.SpiDev()  # Created an object
spi.open(0, 0)

# Define some constants from the datasheet
DEVICE = 0x23  # Default device I2C address

ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21

I2C = smbus.SMBus(1)  # Rev 2 Pi uses 1



# Read MCP3008 data

def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1, (8+channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]

    return data


def readMoist():
    output = analogInput(0)  # Reading from CH0
    output = interp(output, [0, 1023], [100, 0])
    output = int(output)

    return output


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()

    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0

        return round(temp_c, 1)


def convertToNumber(data):

    return ((data[1] + (256 * data[0])) / 1.2)


def readLight(addr=DEVICE):
    data = I2C.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_2)

    return round(convertToNumber(data), 0)


def readHumidity():
    humidity = dhtDevice.humidity

    return humidity


if __name__ == '__main__':
    
    try:
        soil = readMoist() 
    except:
        soil = 0
           
    if soil <= 50:
        count = 0
        try:
            air = readHumidity()
        except:
            air = 1000 
        try:
            light = readLight()
        except:
            light = 0
        try:
            air = readHumidity()
        except:
            air = 0
        
        while air == 0 and count <15:
            sleep(3)
            try:
                air = readHumidity()
            except:
                air = 0
                count+=1
        try:
            temp = read_temp()
        except:
            temp = 0

        # 單位轉換
        
        temp = temp/40
        
        # 載入模型
        
        knn = load('KNNplant.joblib')
        print(knn.predict([[temp, air, light]]))



        conn = mariadb.connect(
        user="tonychen",
        password="killer945",
        host="localhost",
        database="plant")
        cur = conn.cursor()
        now = datetime.now()
        dateTime = now.strftime("%Y-%m-%d,%H:%M:%S")
        # username = request.session.get("user", '')
        # user = User.objects.get(username=username)
        user = 1
        try:
            cur.execute("SELECT pid FROM gui_plant WHERE active = ?",(1,))
            plantIds = cur.fetchall()
            plantId = plantIds[0][0]
            cur.execute("INSERT INTO gui_sensorrecord(create_time,create_user,plant_id,user_id) VALUE(?,?,?,?,)",
                    (dateTime,'10', plantId,user))
        except mariadb.Error as e:
            print(e)

        conn.commit()
        conn.close()

    os.system('pkill libgpiod')
