import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# packages for sending verification email
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages  # import messages

# packages for aquiring data from sensor
import os
import glob
import time
#import spidev  # To communicate with SPI devices
#import smbus
import sys
#import RPi.GPIO as GPIO
from numpy import interp  # To scale values. Mapping value range of 0~1023 to 0~100
from time import sleep


# Global variables for connecting to Sensor

try:
    DEVICE_ADDRESS = 0x23  # Default device I2C address

    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    ONE_TIME_HIGH_RES_MODE_2 = 0x21

    I2C = smbus.SMBus(1)  # 指定使用/dev/i2c-1

    BASE_DIR = '/sys/bus/w1/devices/'
    DEVICE_FOLDER = glob.glob(BASE_DIR + '28*')[0]
    DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'
except :
    print("sensor error")


# 登錄頁面

def login(request):
    return render(request, "login.html")

# 登錄動作

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登錄
            request.session['user'] = username   # 將session資訊記錄到瀏覽器
            return HttpResponseRedirect('/realtime_panel/')
        else:
            messages.error(request, "Username or password error!")
            return render(request, 'login.html')

# 註冊頁面

def register(request):

    return render(request, 'account/register.html')

# 註冊動作

def register_action(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    try:
        user = User.objects.get(username=username)
        messages.error(
            request, "The username is already used. Please change one!")
        return render(request, 'account/register.html')
    except User.DoesNotExist:
        User.objects.create_user(username, email, password)
        messages.success(request, "Register successful. Please login!")
        return render(request, 'login.html')
    # At this point, user is a User object that has already been saved
    # to the database. You can countinue to change its attributes
    # if you want to change other fields.
    # user.last_name = 'Lennon'
    # user.save()

# # 註冊帳號檢查動作
# # preserved for further user check
# def account_check_action(request):
#     username = request.GET.get('username','')
#     user = User.objects.get(username=username)
#     if user is not None:
#         response = "username already exists"
#         return HttpResponse(response)
#     else:
#         response = "you can use this username"
#         return HttpResponse(response)

# 實時資訊頁面

@login_required
def realtime_panel(request):
    username = request.session.get("user", '')
    return render(request, "panel/realtime_panel.html", {"user": username, })

# 統計資訊頁面

@login_required
def statistics_panel(request):
    username = request.session.get("user", '')
    return render(request, "panel/statistics_panel.html", {"user": username, })

# 使用者資料編輯頁面

@login_required
def user_panel(request):
    
    username = request.session.get("user", '')
    useremail = User.objects.get(username=username).email
    plantname= ""
    if not useremail:
        useremail="empty"
    if not plantname:
        plantname="not named yet"
    return render(request, "panel/user_panel.html", {"user": username, "email": useremail, "plantname": plantname})

# 統計資料切換頁面

@login_required
def statistics_panel_shift(request):
    timerange = request.GET.get('timerange', '')
    data = json.dumps({
        "moist": [[0, 0, 2], [1, 2, 3]],
        "temp": [[0, 85], [1, 95]],
        "light": [[0, 85], [1, 95], [2, 36]],
        "pressure": [[0, 25], [1, 95], [2, 125]],
        "watering": [[0, 5], [15, 3]],
    })
    return HttpResponse(data)

# 退出登錄

@login_required
def logout(request):
    auth.logout(request)  # 退出登錄
    return HttpResponseRedirect('/login/')

# 處理帳號重設動作

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '192.168.34.100:8000',
                        'site_name': 'SmartPot',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'tonygood945@gmail.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(
                        request, 'A message with reset password instruction has been sent to your email address.')
                    return HttpResponseRedirect("/login/")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request, "account/password_reset.html", context={"password_reset_form": password_reset_form})

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
        soil_moisture = readMoist()
        light = readLight()
        temp = readTemp() 
    except:
        soil_moisture = "0"
        light = "0"
        temp = "0"


    # Pack the data into dict, then dump into json
    data = {'light': light, 'temp': temp, 'soil': soil_moisture}
    data = json.dumps(data)

    return HttpResponse(data)

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


def readLight(addr=DEVICE_ADDRESS):
    data = I2C.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_2)
    return round(convertToNumber(data), 1)


def readMoist():
    data = analogInput(0)  # Reading from CH0
    data = interp(data, [0, 1023], [100, 0])
    return int(data)
