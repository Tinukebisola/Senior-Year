from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


def landing(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.create_user(email, password1)
            user.save()
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                return redirect('landing')
        else:
            messages.error(request, f"Passwords do not match")
            return redirect('register')
    return render(request, 'login.html')


def loginview(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        user = authenticate(request, email=email, password=password1)
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            existing_user = User.objects.filter(email=email).count()
            if existing_user:
                messages.error(request, f"Password Incorrect")
            else:
                messages.error(request, f"User doesn't exist")
            return redirect('register')
    return render(request, 'login.html')
