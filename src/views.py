from django.shortcuts import redirect, render
from django.contrib import messages
from src.models import Profile
from django.contrib.auth.models import User
from  django.contrib.auth import authenticate,login
from . models import *
import uuid 

from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


def index(request):
    return render(request, "home.html")

def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is added')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Username is added')
                return redirect('/register')


            user_obj = User(username = username , email=email , password=password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_reg(auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)







    return render(request, "register.html" )

def success(request):
    return render(request, "success.html")

def token_send(request):
    return render(request, "token_send.html")

def error_page(request):
    return render(request, 'error.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.success_bol:
                messages.success(request, 'congratulation your email is already being verified')
                return redirect('/login')

            profile_obj.success_bol = True
            profile_obj.save()
            messages.success(request, 'congratulation your email is verified')
            return redirect('/login')
        else:
            return redirect('/error')

    except Exception as e:
        print(e)    


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)

        user_obj = User.objects.filter(username = username).first()
        print(user_obj)
        if user_obj is None:
            print('hiiiiii')
            messages.success(request, 'User not found.')
            return redirect('/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.success_bol:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')
        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')



def send_mail_after_reg(token):
    # subject = 'your account needs to be verified'
    # message = f'paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    # email_from = settings.EMAIL_HOST_USER
    # recepient_list = [email]
    # send_mail(subject, message, email_from, recepient_list) 

    pass