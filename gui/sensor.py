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

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
sleep(1)

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

        return round(temp_c, 0)


def convertToNumber(data):
    return ((data[1] + (256 * data[0])) / 1.2)


def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_2)
    return round(convertToNumber(data), 3)


def readHumidity():
    humidity = dhtDevice.humidity
    return humidity


if __name__ == '__main__':

    conn = mariadb.connect(
        user="tonychen",
        password="killer945",
        host="localhost",
        database="plant")
    cur = conn.cursor()
    try:
        soil = readMoist()
    except:
        soil = 0
    try:
        light = readLight()
    except:
        light = 0
    try:
        air = readHumidity()
    except:
        air = 0
    try:
        temp = read_temp()
    except:
        temp = 0

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d,%H:%M:%S")

    try:
        cur.execute("select plant_id from gui_sensorrecord where active = 1")
        plant_id = cur.fetchall()
        cur.execute("insert into gui_sensorrecord(soil,temperature,air,light,create_time,plant_id) value(?,?,?,?,?,?)",
                (soil, temp, humidity, air, date_time, plant_id[0][0]))
    except mariadb.Error as e:
        print(e)

    conn.commit()
    conn.close()

    os.system('pkill libgpiod')
