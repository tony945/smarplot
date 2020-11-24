from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from gui.models import Plant


# 使用者資料編輯頁面

@login_required
def user_panel(request):
    
    username = request.session.get("user", '')
    useremail = User.objects.get(username=username).email

    if not useremail:
        useremail="empty"

    try:
        plantname = Plant.objects.get(active="1").plant_name
    except:
        plantname="not named yet"


    return render(request, "panel/user_panel.html", {"user": username, "email": useremail, "plantname": plantname})


# 使用者資料編輯頁面-密碼重設

@login_required
def user_panel_password(request):
    username = request.session.get("user", '')
    user = User.objects.get(username=username)
    oldPassword = request.POST.get("oldPassword", '')
    print(oldPassword)
    newPassword = request.POST.get("newPassword", '')
    confirmNewPassword = request.POST.get("confirmPassword", '')
  
    if user.check_password(oldPassword):
        if newPassword == confirmNewPassword:
            user.set_password(newPassword)
            user.save()
            update_session_auth_hash(request, user) # Updates user session to prevent from logging out
            return HttpResponse(0)
        else:
            return HttpResponse(2)
    else:
        return HttpResponse(1)


# 使用者資料編輯頁面-信箱重設

@login_required
def user_panel_email(request):
    newEmail = request.POST.get("newEmail", '')
    if User.objects.filter(email=newEmail):
        return HttpResponse(0)
    else:
        username = request.session.get("user", '')
        user = User.objects.get(username=username)
        user.email = newEmail
        user.save()
        return HttpResponse(1)


# 使用者資料編輯頁面-植物名稱重設

@login_required
def user_panel_plantname(request):
    plantname=request.POST.get("newPlantname", '')
    try:
        plant = Plant.objects.get(active="1")
        plant.plant_name = plantname
        plant.save()
    except:   
        plant = Plant.objects.create(plant_name=plantname)

    return HttpResponse()

 
# 使用者資料編輯頁面-植物重設

@login_required
def user_panel_resetplant(request):
    plant=Plant.objects.get(active="1")
    plant.active="0"
    plant.save()
    return HttpResponse()


# 植物註冊頁面

@login_required
def register_plant(request):
    if Plant.objects.filter(active="1"):
        return HttpResponseRedirect('/realtime_panel/')

    return render(request, "register_plant.html")


# 植物註冊處理

@login_required
def register_plant_action(request):
    plantname =request.POST.get("plantname", '')
    plant = Plant.objects.create(plant_name=plantname)
    return HttpResponseRedirect('/realtime_panel/')