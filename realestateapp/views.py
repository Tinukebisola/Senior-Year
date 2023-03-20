from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User, Apartment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import random
from django.db.models import Q
from django.contrib.auth import logout
from pprint import pprint


def landing(request):
    if request.method == 'POST':
        baths = request.POST.get('baths')
        location = request.POST.get('location')
        budget = request.POST.get('budget')
        rooms = request.POST.get('rooms')
        dogs = request.POST.get('dogs')
        cats = request.POST.get('cats')
        apartments = Apartment.objects.exclude(min_price__isnull=True,
                                               max_price__isnull=True, ).only('pictures', 'pictures1',
                                                                              'min_price', 'max_price',
                                                                              'min_beds', 'max_beds',
                                                                              'min_baths', 'max_baths',
                                                                              'address', 'baths', 'price',
                                                                              'beds', 'state', 'dogs', 'cats')
        if baths:
            apartments = apartments.filter(((Q(min_baths__lte=baths) & Q(max_baths__gte=baths)) | Q(max_baths=baths)))
        if location:
            apartments = apartments.filter(state=location)
        if budget:
            apartments = apartments.filter(
                ((Q(min_price__lte=budget) & Q(max_price__gte=budget)) | Q(max_price=budget)))
        if rooms:
            apartments = apartments.filter(((Q(min_beds__lte=rooms) & Q(max_beds__gte=rooms)) | Q(max_beds=rooms)))
        # if cats:
        #     apartments = apartments.filter(cats=cats)
        #     print(apartments)
        # if dogs:
        #     apartments = apartments.filter(dogs=dogs)
        #     print(apartments)
        apartments = apartments[:16]
    else:
        apartments = Apartment.objects.exclude(min_price__isnull=True,
                                               max_price__isnull=True, ).only('pictures', 'pictures1',
                                                                              'min_price', 'max_price',
                                                                              'min_beds', 'max_beds',
                                                                              'min_baths', 'max_baths',
                                                                              'address', 'baths', 'price',
                                                                              'beds', 'state', 'dogs', 'cats')
        # print(apartments.values()[:16])
        # apartments = apartments[:16]
        apartments = [random.choice(apartments) for i in range(16)]
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'apartments': apartments
    }
    pprint(context)

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
                return redirect('profile')
        else:
            messages.error(request, f"Passwords do not match")
            return redirect('register')
    return render(request, 'login.html')


def loginview(request):
    if request.user.is_authenticated:
        return redirect('landing')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
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


@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'user': request.user if request.user.is_authenticated else None
    }

    return render(request, 'profile.html', context)


def search(request):
    if request.method == 'POST':
        baths = request.POST.get('baths')
        location = request.POST.get('location')
        budget = request.POST.get('budget')
        rooms = request.POST.get('rooms')
        dogs = request.POST.get('dogs')
        cats = request.POST.get('cats')
        apartments = Apartment.objects.filter().only('pictures', 'pictures1',
                                                     'min_price', 'max_price',
                                                     'min_beds', 'max_beds',
                                                     'min_baths', 'max_baths',
                                                     'address', 'baths', 'price',
                                                     'beds', 'state', 'dogs', 'cats')
        if baths:
            apartments = apartments.filter(((Q(min_baths__lte=baths) & Q(max_baths__gte=baths)) | Q(max_baths=baths)))
        if location:
            apartments = apartments.filter(state=location)
        if budget:
            apartments = apartments.filter(
                ((Q(min_price__lte=budget) & Q(max_price__gte=budget)) | Q(max_price=budget)))
        if rooms:
            apartments = apartments.filter(((Q(min_beds__lte=rooms) & Q(max_beds__gte=rooms)) | Q(max_beds=rooms)))
        # if cats:
        #     apartments = apartments.filter(cats=cats)
        #     print(apartments)
        # if dogs:
        #     apartments = apartments.filter(dogs=dogs)
        #     print(apartments)
        apartments = apartments[:16]
    else:
        apartments = Apartment.objects.all().only('pictures', 'pictures1',
                                                  'min_price', 'max_price',
                                                  'min_beds', 'max_beds',
                                                  'min_baths', 'max_baths',
                                                  'address', 'baths', 'price',
                                                  'beds', 'state', 'dogs', 'cats')
        # print(apartments.values()[:16])
        # apartments = apartments[:16]
        apartments = [random.choice(apartments) for i in range(32)]
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'apartments': apartments
    }

    return render(request, 'search.html', context)


def logout_view(request):
    logout(request)
    return redirect('landing')


def property(request, permalink):
    print(permalink)
    apartment = Apartment.objects.filter(permalink=permalink).first()
    context = {}
    return render(request, 'property.html', context)
