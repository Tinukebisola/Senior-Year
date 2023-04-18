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
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import os
import os
import random
from django.templatetags.static import static
from django.conf import settings


def landing(request):
    apartments = Apartment.objects.all().only('pictures', 'pictures1',
                                              'min_price', 'max_price',
                                              'min_beds', 'max_beds',
                                              'min_baths', 'max_baths',
                                              'address', 'baths', 'price',
                                              'beds', 'state', 'dogs', 'cats')
    if request.method == 'POST':
        print(request.POST)
        baths = request.POST.get('baths')
        location = request.POST.get('location')
        budget = request.POST.get('budget')
        rooms = request.POST.get('rooms')
        # dogs = request.POST.get('dogs')
        # cats = request.POST.get('cats')

        if baths:
            apartments = apartments.filter(((Q(min_baths__lte=baths) & Q(max_baths__gte=baths)) | Q(baths=baths)))
        if location != 'State':
            apartments = apartments.filter(state=location)
        if budget:
            apartments = apartments.filter(
                ((Q(min_price__lte=budget) & Q(max_price__gte=budget)) | Q(price=budget)))
        if rooms:
            apartments = apartments.filter(((Q(min_beds__lte=rooms) & Q(max_beds__gte=rooms)) | Q(beds=rooms)))
        # if cats:
        #     apartments = apartments.filter(cats=cats)
        #     print(apartments)
        # if dogs:
        #     apartments = apartments.filter(dogs=dogs)
        #     print(apartments)
        # apartments = apartments[:16]
    # else:
    #     apartments = Apartment.objects.exclude(min_price__isnull=True,
    #                                            max_price__isnull=True, ).only('pictures', 'pictures1',
    #                                                                           'min_price', 'max_price',
    #                                                                           'min_beds', 'max_beds',
    #                                                                           'min_baths', 'max_baths',
    #                                                                           'address', 'baths', 'price',
    #                                                                           'beds', 'state', 'dogs', 'cats')
    # print(apartments.values()[:16])
    # apartments = apartments[:16]
    # apartments = [random.choice(apartments) for i in range(16)]
    storage = []
    apartments = list(apartments)
    random.shuffle(apartments)
    for apartment in apartments:
        if apartment.price > 0:
            storage.append(apartment)
        else:
            if apartment.min_price > 0:
                storage.append(apartment)
        if len(storage) == 16: break
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'apartments': storage
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


# @login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        print(request.FILES.get('profile'), request.POST)
        if request.FILES.get('profile') is not None:
            request.user.profile_picture = request.FILES.get('profile')
        request.user.username = request.POST.get('username')
        request.user.name = request.POST.get('name')
        request.user.gender = request.POST.get('gender')
        request.user.age = request.POST.get('age')
        request.user.pets = request.POST.get('pets')
        request.user.mate = request.POST.get('mate')
        request.user.car = request.POST.get('car')
        request.user.washer = request.POST.get('washer')
        request.user.dryer = request.POST.get('dryer')
        request.user.save()

    context = {
        'user': request.user if request.user.is_authenticated else None
    }

    return render(request, 'profile.html', context)


def search(request):
    apartments = Apartment.objects.all().only('pictures', 'pictures1',
                                              'min_price', 'max_price',
                                              'min_beds', 'max_beds',
                                              'min_baths', 'max_baths',
                                              'address', 'baths', 'price',
                                              'beds', 'state', 'dogs', 'cats')
    if request.method == 'POST':
        baths = request.POST.get('baths')
        location = request.POST.get('location')
        budget = request.POST.get('budget')
        rooms = request.POST.get('rooms')
        dogs = request.POST.get('dogs')
        cats = request.POST.get('cats')

        if baths:
            apartments = apartments.filter(((Q(min_baths__lte=baths) & Q(max_baths__gte=baths)) | Q(baths=baths)))
        if location != 'State':
            apartments = apartments.filter(state=location)
        if budget:
            apartments = apartments.filter(
                ((Q(min_price__lte=budget) & Q(max_price__gte=budget)) | Q(price=budget)))
        if rooms:
            apartments = apartments.filter(((Q(min_beds__lte=rooms) & Q(max_beds__gte=rooms)) | Q(beds=rooms)))
        # if cats:
        #     apartments = apartments.filter(cats=cats)
        #     print(apartments)
        # if dogs:
        #     apartments = apartments.filter(dogs=dogs)
        #     print(apartments)
        # apartments = apartments[:16]
    storage = []
    apartments = list(apartments)
    random.shuffle(apartments)
    for apartment in apartments:
        if apartment.price > 0:
            storage.append(apartment)
        else:
            if apartment.min_price > 0:
                storage.append(apartment)
        if len(storage) == 16: break
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'apartments': storage
    }

    return render(request, 'search.html', context)


def logout_view(request):
    logout(request)
    return redirect('landing')


def get_page_content(url, timeout):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print(f'Timeout reached after {timeout} seconds.')
    content = driver.page_source
    driver.quit()
    return content


def property(request, permalink):
    # print(permalink)
    apartment = Apartment.objects.filter(permalink=permalink).first()
    url = f'https://www.realtor.com/realestateandhomes-detail/{permalink}'
    storage = {}
    scrape = False
    mate = {
        'pets': False,
        'garage': False,
        'dryer': False,
        'washer': False,
        'roommate': False
    }
    if scrape:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        if settings.APP:
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                                      chrome_options=chrome_options)
        else:
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        driver.get(url)
        try:
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
            WebDriverWait(driver, 5000).until(element_present)
        except TimeoutException:
            print(f'Timeout reached after 5000 seconds.')
        content = driver.page_source
        driver.quit()
        soup = BeautifulSoup(content, 'html.parser')
        counter = 0

        scripts = soup.find_all('script')
        for script_tag in scripts:
            if 'id' in script_tag.attrs and script_tag.attrs['id'] == '__NEXT_DATA__':
                page = json.loads(script_tag.text)
                for feature in page['props']['pageProps']['property']['details']:
                    # storage[feature['category']] = feature['text']
                    if request.user.is_authenticated:
                        for feat in feature['text']:
                            if request.user.pets:
                                if (
                                        'dog' in feat.lower() or 'cat' in feat.lower()) and 'allowed' in feat.lower() and not 'not' in feat.lower() and not \
                                        mate['pets']:
                                    mate['pets'] = True
                                    counter += 1
                            else:
                                counter += 1
                            if request.user.washer:
                                if 'washer' in feat.lower() and not mate['washer']:
                                    mate['washer'] = True
                                    counter += 1
                            else:
                                counter += 1
                            if request.user.dryer:
                                if 'dryer' in feat.lower() and not mate['dryer']:
                                    mate['dryer'] = True
                                    counter += 1
                            else:
                                counter += 1
                            if request.user.car:
                                if 'garage' in feat.lower() and not mate['garage']:
                                    mate['garage'] = True
                                    counter += 1
                            else:
                                counter += 1

                    num = len(feature['text']) // 2
                    storage[feature['category']] = []
                    storage[feature['category']].append(feature['text'][:num + 1])
                    storage[feature['category']].append(feature['text'][num + 1:])
                # pprint(storage)
                # print(counter)
                # print(content)
                break

    context = {}
    context['apartment'] = apartment
    context['storage'] = storage
    random_profiles = [
        {
            'name': 'Jennifer Johnson',
            'age': 27,
            'sex': 'Female',
            'img': static('assets/img/profile/girl.jpg')
        },
        {
            'name': 'Natalie Robinson',
            'age': 25,
            'sex': 'Female',
            'img': static('assets/img/profile/girl1.jpg')
        },
        {
            'name': 'John Ferguson',
            'age': 18,
            'sex': 'Male',
            'img': static('assets/img/profile/guy1.jpg')
        },
        {
            'name': 'Samuel Patterson',
            'age': 19,
            'sex': 'Male',
            'img': static('assets/img/profile/guy.jpg')
        },
        {
            'name': 'Jasmine James',
            'age': 22,
            'sex': 'Female',
            'img': static('assets/img/profile/girl2.jpg')
        }]
    random.shuffle(random_profiles)
    # context['match'] = (counter / 4) * 100
    # context['preference'] = mate
    context.update(mate)
    # context['match'] = 100
    context['random_profiles'] = random_profiles[:3]
    # print(context)
    # context.update(storage)
    return render(request, 'property.html', context)
