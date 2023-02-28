from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User, Apartment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import random
from django.contrib.auth import logout


def landing(request):
    apartments = Apartment.objects.all().only('pictures', 'pictures1',
                                              'min_price', 'max_price',
                                              'min_beds', 'max_beds',
                                              'min_baths', 'max_baths',
                                              'address')
    apartments = [random.choice(apartments) for i in range(20)]
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'apartments': apartments
    }
    return render(request, 'index.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')

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
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            existing_user = User.objects.filter(email=email).count()
            if existing_user:
                messages.error(request, f"Password Incorrect")
            else:
                messages.error(request, f"User doesn't exist")
            return redirect('register')
    return render(request, 'login.html')


@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'user': request.user if request.user.is_authenticated else None
    }

    return render(request, 'profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('landing')
