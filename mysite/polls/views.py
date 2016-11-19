from django.shortcuts import render, redirect, HttpResponseRedirect
from mongoengine.errors import NotUniqueError, ValidationError
from django.core.paginator import Paginator
from django.conf import settings

from polls.models import User, Film
import math, hashlib, datetime, os

def make_password(password):
    salt = '&e2g$jR-%/frwR0()2>d#'
    hash = hashlib.md5(bytes(password + salt, encoding = 'utf-8')).hexdigest()
    return hash

def check_password(hash, password):
    generated_hash = make_password(password)
    return hash == generated_hash

def save_file(f, root):
    path = os.path.join(settings.BASE_DIR + settings.MEDIA_URL, root)
    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return str(root + '/' + f.name)

# Create your views here.

def error(request):
    return render(request, 'html/Error.html', {'error': '404 Not Found!'})

def home(request):
    if request.method == 'GET':
        if 'id' in request.session:
            return render(request, 'html/home.html', {'registered': True})
        else:
            return render(request, 'html/home.html', {'registered': False})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def signup(request):
    if request.method == 'GET':
        return render(request, 'html/signup.html', {})
    elif request.method == 'POST':
        name = ' '.join(request.POST.get('name', '').strip().split()) # убирает пробелы beg-end; несколько пробелов заменяются одним
        mail = request.POST.get('mail', '').replace(' ', '')
        password_1 = request.POST.get('password_1', '').replace(' ', '')
        password_2 = request.POST.get('password_2', '').replace(' ', '')

        if name and mail and password_1 and password_2:
            if password_1 == password_2:
                try:
                    password = make_password(password_1)
                    User.objects.create(name = name, mail = mail, password = password)
                    # user, created = User.objects.get_or_create(mail = mail, defaults = {'name': name, 'password': password_1})
                    return render(request, 'html/login.html', {})
                except NotUniqueError:
                    return render(request, 'html/Error.html', {'error': 'Mail уже существует!'})
                except ValidationError:
                    return render(request, 'html/Error.html', {'error': 'Некорректный ввод mail!'})
                except:
                    return render(request, 'html/Error.html', {'error': 'Неизвестная ошибка!'})
            else:
                return render(request, 'html/Error.html', {'error': 'Пароли не совпадают!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

#new
def login(request):
    if request.method == 'GET':
        return render(request, 'html/login.html', {})
    elif request.method == 'POST':
        mail = request.POST.get('mail', '').replace(' ', '')
        password = request.POST.get('password', '').replace(' ', '')

        if mail and password:
            try:
                user = User.objects.get(mail = mail)
                if check_password(user.password, password):
                    request.session['id'] = str(user.id)
                    return render(request, 'html/home.html', {'registered': True})
                else:
                    return render(request, 'html/Error.html', {'error': 'Неверный пароль!'})
            except:
                return render(request, 'html/Error.html', {'error': 'Неверный mail!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

#new
def logout(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return render(request, 'html/home.html', {'registered': False})

def restore(request):
    if request.method == 'GET':
        return render(request, 'html/restore.html', {})
    elif request.method == 'POST':
        return render(request, 'html/restore.html', {})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def films(request, page_number):
    if request.method == 'GET':
        value = ' '.join(request.GET.get('value', '').strip().split())
        count_films_on_page = 4

        if not value:
            films = Film.objects.all()
        else:
            films = Film.objects.filter(name__icontains = value)

        if int(page_number) >= 1 and int(page_number) <= math.ceil(len(films) / count_films_on_page):
            current_page = Paginator(films, count_films_on_page)
            return render(request, 'html/films.html', {'films': current_page.page(page_number), 'ismyfilms': False})
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

# TODO:
def rating(request): # переделать
    if request.method == 'POST':
        name = ' '.join(request.POST.get('name', '').strip().split())
        grade = request.POST.get('grade', '').replace(' ', '')

        #film = Film.objects.get(name = name)

        #user = User.objects.get(films = film)
        #user.update(add_to_set__films = {'grade': 12})

        if name and grade:
            if 'id' in request.session:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)

                    #user.update(set__films__grade = grade)

                    #Film.objects(name = name).update(set__film = grade) # изменить бд, проверки
                    return redirect('/filminfo/' + name)
                except:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            else:
                return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# должен работать!!! проверить на уникальность
def add(request):
    if request.method == 'POST':
        name = ' '.join(request.POST.get('name', '').strip().split())

        if name:
            if 'id' in request.session:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    film = Film.objects.get(name = name)
                    myfilm = {'film': film, 'grade': 0, 'date': datetime.datetime.now()}
                    user.update(add_to_set__films = myfilm)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
                except:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            else:
                return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# TODO:
def sort(request):
    if request.method == 'GET':
        value = ' '.join(request.GET.get('value', '').strip().split())

        if value:
            if 'id' in request.session:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)

                    #people = User.objects.order_by('-grade')    # поправить
                    #for p in people:
                        #print(p.name + '   ' + p.mail)

                    return render(request, 'html/Error.html', {'error': 'Ок!'}) # изменить страницу
                except:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            else:
                return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# должен работать!!!
def myfilms(request, page_number):
    if request.method == 'GET':
        value = ' '.join(request.GET.get('value', '').strip().split())
        count_films_on_page = 4

        if 'id' in request.session:
            try:
                user_id = request.session.get('id')
                user = User.objects.get(id = user_id)

                if not value:
                    films = user.films
                else:
                    films = list(filter(lambda film: film['film'].name == value, user.films))

                if int(page_number) >= 1 and int(page_number) <= math.ceil(len(films) / count_films_on_page):
                    current_page = Paginator(films, count_films_on_page)
                    return render(request, 'html/films.html', {'films': current_page.page(page_number), 'ismyfilms': True})
                else:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            except:
                return render(request, 'html/Error.html', {'error': '404 Not Found!'})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# должен работать!!!
def addfilm(request):
    if request.method == 'GET':
        if 'id' in request.session:
            user_id = request.session.get('id')
            user = User.objects.get(id = user_id)

            if user.role == 'admin':
                return render(request, 'html/addfilm.html', {})
            else:
                return render(request, 'html/Error.html', {'error': '403 Forbidden!'})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    elif request.method == 'POST':
        name = request.POST.get('name', '').strip()
        name = ' '.join(name.split()) # несколько пробелов заменяются одним
        image = save_file(request.FILES['image'], 'image')
        about = request.POST.get('about', '').replace(' ', '')
        country = request.POST.get('country', '').replace(' ', '')
        year = request.POST.get('year', '').replace(' ', '')
        genre = request.POST.get('genre', '').replace(' ', '')
        duration = request.POST.get('duration', '').replace(' ', '')
        producer = request.POST.get('producer', '').replace(' ', '')
        actors = request.POST.get('actors', '').replace(' ', '')
        video = save_file(request.FILES['video'], 'video')

        if 'id' in request.session:
            user_id = request.session.get('id')
            user = User.objects.get(id = user_id)

            if user.role == 'admin':
                if name and image and about and country and year and genre and duration and producer and actors and video:
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
                            video = video
                        )
                        # get_or_create
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
                    except:
                        return render(request, 'html/Error.html', {'error': 'Неверный ввод!'})
                else:
                    return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
            else:
                return render(request, 'html/Error.html', {'error': '403 Forbidden!'})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})
