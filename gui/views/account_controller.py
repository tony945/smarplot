from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from gui.models import Plant
from django.contrib import messages  # import messages

# Packages for sending verification email
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


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
            if Plant.objects.filter(active="1"):
                return HttpResponseRedirect('/realtime_panel/')
            else:
                return HttpResponseRedirect('/register_plant/')
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
        messages.error(request, "The username is already used. Please change one!")
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
