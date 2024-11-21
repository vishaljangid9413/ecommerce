import json
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required

from utils.otp_handler import OTPHandler
import traceback
from .models import User
from .forms import RegistrationForm
import environ
env = environ.Env()


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'accounts/login.html')


def register_page(request):
    form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def registeration_form(request):
    otp = request.POST.get('otp')
    name = request.POST.get('name')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    password = request.POST.get('password')
    try:
        if request.method != 'POST':
            raise ValueError("Only POST Method Allowed")

        # Check if user exists with same phone number
        user = User.objects.filter(mobile=mobile).first()
        if user:
            login(request, user)
            return redirect('/')

        # verify otp 
        OTPHandler.verifyOTP(email, otp)
        
        # Create new user
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(password)
            user.save()
        else:
            raise ValueError(form.errors)

        messages.success(request, 'Registeration Successfull')
        login(request, user)
        return redirect('/')
    except Exception as e:
        traceback.print_exc()
        messages.error(request, str(e))
        form = RegistrationForm(initial={'name': name, 'email': email, 'mobile': mobile, 'password':password})
        return render(request, 'accounts/register.html', {'form': form})


def login_form(request):
    mobile = request.POST.get('mobile')
    password = request.POST.get('password')
    try:
        if request.method != 'POST':
            raise ValueError("Only POST Method Allowed")
        
        user = User.objects.filter(mobile=mobile).first()
        if not user:
            raise ValueError("User Not Found")
        
        if not user.check_password(password):
            raise ValueError('Invalid user & password combination')
        
        auth = authenticate(mobile=mobile, password=password) 
        if auth is None:
            raise ValueError("Authentication Failed")
        login(request, user)
        return redirect('/')
    except Exception as e:
        traceback.print_exc()
        messages.error(request, str(e))
        return render(request, 'accounts/login.html', {'mobile': mobile})


def logout(request):
    auth_logout(request)
    return redirect("/login/")


@login_required
def profile_page(request):
    return render(request, 'accounts/profile.html')


@login_required
def user_list(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/categories/')
    
    users = User.objects.filter(is_superuser=False, is_deleted=False).order_by('-registration_datetime')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def toggle_user_status(request, pk):
    try:
        if not request.user.is_superuser:
            return ValueError("You are not authorized to update user status.")
        
        user = User.objects.filter(pk=pk).first()
        if not user:
            raise ValueError("User not found!")
        
        user.is_active = not user.is_active
        user.save()
        return redirect('user_list')
    except Exception as e:
        traceback.print_exc()
        messages.error(request, str(e))
        return redirect('/categories/')


@login_required
def delete_user(request, pk):
    try:
        if not request.user.is_superuser:
            return ValueError("You are not authorized to delete this user.")
        
        user = User.objects.filter(pk=pk).first()
        if not user:
            raise ValueError("User not found!")
        
        user.is_deleted = not user.is_deleted
        user.save()
        return redirect('user_list')
    except Exception as e:
        traceback.print_exc()
        messages.error(request, str(e))
        return redirect('/categories/')



def get_otp(request):
    if request.method == 'POST':
        # can be accessed from ajax or postman 
        email = request.GET.get("email")
        data = json.loads(request.body)
        email = data['email']
        print("Note::", email)
        try:            
            otp = OTPHandler.generate_otp(email) 
            print("OTP: ",otp)
            return JsonResponse({'otp':otp})       
        except Exception as e:
            traceback.print_exc()
            return HttpResponseBadRequest(str(e))

