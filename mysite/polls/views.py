from django.shortcuts import render, redirect
from django.http import QueryDict
from pymongo import MongoClient

from django.core.paginator import Paginator
from mongoengine.errors import NotUniqueError, ValidationError

#from django.contrib.auth.hashers import *
"""a = make_password(password = 'testing', salt = '123')
b = make_password(password = 'testing')
print(a)
print(b)
print ( check_password('testing', a))
print ( check_password('testing', b))"""

from polls.models import User, Film
import math, hashlib
import random, json

def make_password(password):
    salt = '&e2g$jR-%/frwR0()2>d#'
    hash = hashlib.md5(bytes(password + salt, encoding = 'utf-8')).hexdigest()
    return hash

def check_password(hash, password):
    generated_hash = make_password(password)
    return hash == generated_hash

# Create your views here.

def home(request):
    if request.method == 'GET':
        return render(request, 'html/home.html', {})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def signup(request):
    if request.method == 'GET':
        return render(request, 'html/signup.html', {})
    elif request.method == 'POST':
        name = request.POST.get('name', '').strip()
        name = ' '.join(name.split()) # несколько пробелов заменяются одним
        mail = request.POST.get('mail', '').replace(' ', '')
        password_1 = request.POST.get('password_1', '').replace(' ', '')
        password_2 = request.POST.get('password_2', '').replace(' ', '')

        if name and mail and password_1 and password_2:
            if password_1 == password_2:
                try:
                    password = make_password(password_1)
                    User.objects.create(name = name, mail = mail, password = password)
                    # user, created = User.objects.get_or_create(mail = mail, defaults = {'name': name, 'password': password_1})
                    return render(request, 'html/signin.html', {})
                except NotUniqueError:
                    return render(request, 'html/Error.html', {'error': 'Mail уже существует!'})
                except ValidationError:
                    return render(request, 'html/Error.html', {'error': 'Некорректный ввод mail или пароля!'})
                except:
                    return render(request, 'html/Error.html', {'error': 'Неизвестная ошибка!'})
            else:
                return render(request, 'html/Error.html', {'error': 'Пароли не совпадают!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def signin(request):
    if request.method == 'GET':
        return render(request, 'html/signin.html', {})
    elif request.method == 'POST':
        mail = request.POST.get('mail', '').replace(' ', '')
        password = request.POST.get('password', '').replace(' ', '')

        if mail and password:
            try:
                user = User.objects.get(mail = mail)
                if check_password(user.password, password):
                    return render(request, 'html/home.html', {})
                else:
                    return render(request, 'html/Error.html', {'error': 'Неверный пароль!'})
            except:
                return render(request, 'html/Error.html', {'error': 'Неверный mail!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def restore(request):
    if request.method == 'GET':
        return render(request, 'html/restore.html', {})
    elif request.method == 'POST':
        pass
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def films(request, page_number):
    if request.method == 'GET':
        count_films_on_page = 4
        maxCount = Film.objects.count()

        if int(page_number) >= 1 and int(page_number) <= math.ceil(maxCount / count_films_on_page):
            films = Film.objects.all()
            current_page = Paginator(films, count_films_on_page)
            return render(request, 'html/films.html', {'films': current_page.page(page_number)})
        else:
            return render(request, 'html/Error.html', {'error': '404 Not Found!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def filminfo(request, name):
    if request.method == 'GET':
        try:
            film = Film.objects.get(name = name)
            return render(request, 'html/filminfo.html', {'film': film})
        except:
            return render(request, 'html/Error.html', {'error': '404 Not Found!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})





def addfilm(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        name = ' '.join(name.split()) # несколько пробелов заменяются одним
        image = request.POST.get('image', '').replace(' ', '')
        about = request.POST.get('about', '').replace(' ', '')
        country = request.POST.get('country', '').replace(' ', '')
        year = request.POST.get('year', '').replace(' ', '')
        genre = request.POST.get('genre', '').replace(' ', '')
        duration = request.POST.get('duration', '').replace(' ', '')
        producer = request.POST.get('producer', '').replace(' ', '')
        actors = request.POST.get('actors', '').replace(' ', '')
        film = request.POST.get('film', '').replace(' ', '')

        if name and image and about and country and year and genre and duration and producer and actors and film:
            try:
                film = Film.objects.create(
                    name = name,
                    image = image,
                    about = about,
                    country = country,
                    year = year,
                    genre = genre,
                    duration = duration,
                    producer = producer,
                    actors = actors,
                    film = film
                )
                # get_or_create
                return render(request, 'html/films.html', {})
            except:
                return render(request, 'html/Error.html', {'error': 'Неверный ввод!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})






######
def check_keys(body, keys):
    if len(body.keys()) != len(keys):
        return False

    for key in body.keys():
        for i in range(len(keys)):
            if key == keys[i]:
                keys.pop(i)
                break

    if len(keys) != 0:
        return False

    for key in body.keys():
        if not body.get(key).replace(' ', ''):
            return False

    return True
######

def index(request):
    return render(request, 'html/index.html', {})

def all(request):
    client = MongoClient()
    collection = client.lab4.sm

    ScrumMasters = []
    for i in collection.find():
        ScrumMasters.append(i)

    client.close();
    return render(request, 'html/all.html', {'rows': ScrumMasters})

def scrum(request, id):
    client = MongoClient()
    collection = client.lab4.sm
    ScrumMaster = collection.find_one({'id': id})
    maxCount = collection.count()
    client.close();

    if int(id) >= 1 and int(id) <= maxCount:
        return render(request, 'html/scrum.html', {'sm': ScrumMaster})
    else:
        return render(request, 'html/Error.html', {})


# lab5:
def new(request):
    if request.method == 'GET':
        id = random.randint(1, 5)
        img = "sm_" + str(id) + ".jpg"
        return render(request, 'html/new.html', {'image': img})
    elif request.method == 'POST':
        req_body = request.body.decode('utf-8')
        new = QueryDict(req_body)

        client = MongoClient()
        collection = client.test.scrum_master

        if not new['name'].replace(' ', '') or not new['surname'].replace(' ', ''):
            client.close();
            return render(request, 'html/Error.html', {})

        collection.insert ({
            'id': str(collection.count() + 1),
            'name': new['name'].title(),
            'surname': new['surname'].title(),
            'date': new['date'],
            'count': new['count'],
            'score': new['score'],
            'img': new['img']
        })

        client.close();
        return redirect('/all.html')

def edit(request, id):
    client = MongoClient()
    collection = client.lab4.sm
    ScrumMaster = collection.find_one({'id': id})
    maxCount = collection.count()

    if int(id) >= 1 and int(id) <= maxCount:
        if request.method == 'GET':
            client.close();
            return render(request, 'html/edit.html', {'sm': ScrumMaster})
        elif request.method == 'POST':
            req_body = request.body.decode('utf-8')
            edit = QueryDict(req_body)

            if not edit['name'].replace(' ', '') or not edit['surname'].replace(' ', ''):
                client.close();
                return render(request, 'html/Error.html', {})

            collection.update ({'id': id}, {
                'id': id,
                'name': edit['name'].title(),
                'surname': edit['surname'].title(),
                'date': edit['date'],
                'count': edit['count'],
                'score': edit['score'],
                'img': edit['img']
            })

            client.close();
            return redirect('/scrum/' + id + '.html')
    else:
        client.close();
        return render(request, 'html/Error.html', {})

def delete(request, id):
    client = MongoClient()
    collection = client.test.scrum_master
    ScrumMaster = collection.find_one({'id': id})
    maxCount = collection.count()

    if int(id) >= 1 and int(id) <= maxCount:
        collection.remove({'id': id})

        client.close();
        return redirect('/all.html')
    else:
        client.close();
        return render(request, 'html/Error.html', {})
