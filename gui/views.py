from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages #import messages

# Create your views here.

def login(request):
    return render(request, "login.html")

# 登錄動作

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None :
            auth.login(request, user)  # 登錄
            request.session['user'] = username    # 將 session 資訊記錄到瀏覽器
            
            return HttpResponseRedirect('/realtime_panel/')
        else:
            return render(request, 'login.html', {'hint': 'Username or password error!'})

# 註冊頁面

def register(request):

    return render(request,'register.html')

# 註冊動作

def register_action(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email','')
    user = User.objects.create_user(username,email,password)

    # At this point, user is a User object that has already been saved 
    # to the database. You can countinue to change its attributes
    # if you want to change other fields.
    # user.last_name = 'Lennon'
    # user.save() 
    return render(request, 'login.html', {'hint': 'Register successful. Please login!'})

# 註冊帳號檢查動作

def account_check_action(request):
    username = request.GET.get('username','')
    user = User.objects.get(username=username)
    if user is not None:
        response = "username already exists"
        return HttpResponse(response)
    else:
        response = "you can use this username"
        return HttpResponse(response)

# 實時資訊頁面

@login_required
def realtime_panel(request):
    username = request.session.get("user", '')
    return render(request, "realtime_panel.html", {"user":username,})

# 統計資訊頁面

@login_required
def statistics_panel(request):
    username = request.session.get("user", '')
    return render(request, "statistics_panel.html", {"user":username,})

# 統計資料切換頁面

@login_required
def statistics_panel_shift(request):
    timerange = request.GET.get('timerange','')
    data = json.dumps({
        "moist":[[0,0,2],[1,2,3]],
        "temp":[[0,85],[1,95]],
        "light":[[0,85],[1,95],[2,36]],
        "pressure":[[0,25],[1,95],[2,125]],
        "watering":[[0,5],[15,3]],
        }) 
    return HttpResponse(data)

# 退出登錄

@login_required
def logout(request):
    auth.logout(request) # 退出登錄
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
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'192.168.34.100:8000',
                    'site_name': 'SmartPot',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'tonygood945@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instruction has been sent to your email address.')
                    return HttpResponseRedirect("/login/")
            messages.reset.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

# 處理及時資訊更新

@login_required
def realtime_data_refresh(request):
    return HttpResponse(data)

