from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistationForm
from django.contrib.auth.decorators import login_required

import os
import subprocess
import time

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
            form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    executed = 'notdone'
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_from.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

def init(request):
    if request.method == 'GET':
        # 初始化kubeflow
        dashboard_url = 'none'
        if request.GET.get('init_kubeflow'):
            SCRIPT_PATH = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
            subprocess.Popen(["/bin/bash", SCRIPT_PATH + '/__init__.sh'])
            time.sleep(3)
            return render(request, 'account/dashboard.html', {'dashboard_url': dashboard_url})
        else:
            # 打开dashboard或者notebook
            print("open dashboard")
            try:
                out = subprocess.check_output(['minikube', 'dashboard', '--url'])
            except:
                return render(request, 'account/dashboard.html')
            print('out:' + bytes.decode(out))
            dashboard_url = bytes.decode(out)
            if dashboard_url[0:4] != 'http':
                dashboard_url = 'none'
                return render(request, 'account/dashboard.html', {'dashboard_url': dashboard_url})
            else:
                return render(request, 'account/dashboard.html', {'dashboard_url': dashboard_url})
    return render(request, 'account/dashboard.html')
