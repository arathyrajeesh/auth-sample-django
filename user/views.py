from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already exists'})
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')   
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    return render(request, 'register.html')


def login_view(request):  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)   
            return redirect('dashboard')  
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
            
    return render(request, 'login.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html', {"username": request.user.username})


def logout_view(request):
    auth_logout(request)  
    return redirect('login')
