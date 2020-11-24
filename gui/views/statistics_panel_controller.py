from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json


# 統計資訊頁面

@login_required
def statistics_panel(request):
    username = request.session.get("user", '')
    return render(request, "panel/statistics_panel.html", {"user": username, })


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
