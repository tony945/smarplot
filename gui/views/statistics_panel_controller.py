from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
import json
from datetime import date
from gui.models import Plant, SensorRecord, DailySensorRecord, MonthlySensorRecord


# 統計資訊頁面

@login_required
def statistics_panel(request):
    username = request.session.get("user", '')
    
    return render(request, "panel/statistics_panel.html", {"user": username,})


# 統計資料切換頁面

@login_required
def statistics_panel_shift(request):
    timerange = request.GET.get('timerange', '')
    today = date.today()
    plantObj = Plant.objects.get(active="1")
    if timerange == 'day':
        formatToday= today.strftime("%Y-%m-%d")
        SensorRecordObj = SensorRecord.objects.filter(plant_id = plantObj.pid).filter(create_time__startswith='{}'.format(formatToday))
    elif timerange == 'month':
        formatToday= today.strftime("%Y-%m")
        SensorRecordObj = DailySensorRecord.objects.filter(plant_id = plantObj.pid).filter(create_time__startswith='{}'.format(formatToday))
    elif timerange == 'year':
        formatToday= today.strftime("%Y")
  
        SensorRecordObj = MonthlySensorRecord.objects.filter(plant_id = plantObj.pid).filter(create_time__startswith='{}'.format(formatToday))
    
    data = list(SensorRecordObj.values())

    return JsonResponse(data, safe=False)
