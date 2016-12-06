from django.shortcuts import render, redirect, HttpResponseRedirect
from mongoengine.errors import NotUniqueError, ValidationError
from django.core.paginator import Paginator
from django.conf import settings

from polls.models import User, Film
import math, hashlib, datetime, os

count_films_on_page = 10

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

# Добавить к ошибкам аргументы !!!

def error(request):
    if request.method == 'GET':
        if 'id' in request.session:
            return render(request, 'html/Error.html', {'error': '404 Not Found!', 'registered': True})
        else:
            return render(request, 'html/Error.html', {'error': '404 Not Found!', 'registered': False})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def home(request):
    if request.method == 'GET':
        if 'id' in request.session:
            #user_id = request.session.get('id')
            #user = User.objects.get(id = user_id)
            #user.delete()
            return render(request, 'html/home.html', {'registered': True})
        else:
            return render(request, 'html/a.html', {'registered': False})
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
                    return redirect('/', {'registered': True})
                else:
                    return render(request, 'html/Error.html', {'error': 'Неверный пароль!'})
            except:
                return render(request, 'html/Error.html', {'error': 'Неверный mail!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# DONE
def logout(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return redirect('/', {'registered': False})

def restore(request):
    if request.method == 'GET':
        return render(request, 'html/restore.html', {})
    elif request.method == 'POST':
        return render(request, 'html/restore.html', {})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# DONE (переписать ошибки)
def films(request, page_number):
    if request.method == 'GET':
        value = ' '.join(request.GET.get('value', '').strip().split())

        if not value:
            films = Film.objects.all()
            args = {'search': ''}
        else:
            films = Film.objects.filter(name__icontains = value)
            args = {'search': value}

        if int(page_number) >= 1 and int(page_number) <= math.ceil(len(films) / count_films_on_page):
            current_page = Paginator(films, count_films_on_page)

            if 'id' in request.session:
                args.update({'films': current_page.page(page_number), 'registered': True, 'ismyfilms': False})
            else:
                args.update({'films': current_page.page(page_number), 'registered': False, 'ismyfilms': False})

            return render(request, 'html/films.html', args)
        else:
            return render(request, 'html/Error.html', {'error': '404 Not Found!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# name__icontains -> name (? не отправляет как символ)
def filminfo(request, name):
    if request.method == 'GET':
        try:
            film = Film.objects.get(name = name)

            if 'id' in request.session:
                args = {'film': film, 'registered': True, 'ismyfilms': False}
            else:
                args = {'film': film, 'registered': False, 'ismyfilms': False}

            return render(request, 'html/filminfo.html', args)
        except:
            return render(request, 'html/Error.html', {'error': '404 Not Found!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})


# demo
def delmyfilms(request):
    if request.method == 'GET':
        if 'id' in request.session:
            try:
                user_id = request.session.get('id')
                user = User.objects.get(id = user_id)
                user.update(set__films = [])
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
            except:
                return render(request, 'html/Error.html', {'error': '404 Not Found!'})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# demo (протестировать)
def delete(request):
    if request.method == 'POST':
        name = ' '.join(request.POST.get('name', '').strip().split())

        if name:
            if 'id' in request.session:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    film = Film.objects.get(name__icontains = name)

                    for f in user.films:
                        if film == f['film']:
                            user.update(pull__films = f)
                            break

                    return redirect('/myfilms/page/1', {'registered': True})
                except:
                    return render(request, 'html/Error.html', {'error': 'sad404 Not Found!'})
            else:
                return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# admin
def d(request, name):
    film = Film.objects.get(name = name)
    film.delete()
    print('#'*50)
    return render(request, 'html/films.html', {'registered': True})

# должен работать!!! не всегда работает !!!
def rating(request): # переделать
    if request.method == 'POST':
        name = ' '.join(request.POST.get('name', '').strip().split())
        grade = request.POST.get('grade', '').replace(' ', '')

        if name and grade and grade.isdigit():
            if 'id' in request.session:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    film = Film.objects.get(name = name)

                    for f in user.films:
                        if film == f['film']:
                            updated = dict(date = f['date'], film = f['film'], grade = grade)
                            user.update(pull__films = f)
                            user = User.objects.get(id = user_id)
                            user.update(add_to_set__films = updated)
                            break

                    return render(request, 'html/home.html', {'registered': True})
                except:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            else:
                return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# должен работать!!!
def sort(request):
    if request.method == 'GET':
        value = ' '.join(request.GET.get('value', '').strip().split())

        #films = user.films[0]['film']
        #films.sort(key = lambda x: x.year)

        if value:
            if 'id' in request.session:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    films = user.films

                    if value == 'grade' or value == 'date':
                        films.sort(key = lambda x: x[value], reverse = True)
                    else:
                        return render(request, 'html/Error.html', {'error': 'Not Value!'})

                    return render(request, 'html/sortedfilms.html', {'films': films}) # изменить страницу
                except:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            else:
                return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# должен работать!!!
def add(request):
    if request.method == 'POST':
        name = ' '.join(request.POST.get('name', '').strip().split())

        if name:
            if 'id' in request.session:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    film = Film.objects.get(name = name)

                    for f in user.films:
                        if film == f['film']:
                            return render(request, 'html/Error.html', {'error': 'Фильм уже был добавлен!'})

                    myfilm = {'film': film, 'grade': '0', 'date': datetime.datetime.now()}
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

# DONE (переписать ошибки)
def myfilms(request, page_number):
    if request.method == 'GET':
        value = ' '.join(request.GET.get('value', '').strip().split())

        if 'id' in request.session:
            #try:
            user_id = request.session.get('id')
            user = User.objects.get(id = user_id)

            if not value:
                films = user.films
                args = {'search': ''}
            else:
                films = list(filter(lambda film: film['film'].name.lower().find(value.lower()) != -1, user.films))
                args = {'search': value}

            if int(page_number) >= 1 and int(page_number) <= math.ceil(len(films) / count_films_on_page):
                current_page = Paginator(films, count_films_on_page)
                args.update({'films': current_page.page(page_number), 'registered': True, 'ismyfilms': True})
                return render(request, 'html/films.html', args)
            else:
                return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            #except:
                #return render(request, 'html/Error.html', {'error': '404 Not Found!'})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def myfilminfo(request, name):
    if request.method == 'GET':
        if 'id' in request.session:
            try:
                user_id = request.session.get('id')
                user = User.objects.get(id = user_id)

                film = Film.objects.get(name = name)

                for f in user.films:
                    if film == f['film']:
                        f['date'] = f['date'].strftime('%d:%m:%Y')
                        return render(request, 'html/filminfo.html', {'film': f, 'registered': True, 'ismyfilms': True})

                return render(request, 'html/Error.html', {'error': 'Film Not Found!'})
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
        try:
            name = request.POST.get('name', '').strip()
            name = ' '.join(name.split()) # несколько пробелов заменяются одним
            image = save_file(request.FILES['image'], 'image')
            about = request.POST.get('about', '').strip()
            about = ' '.join(about.split()) # несколько пробелов заменяются одним
            country = request.POST.get('country', '').strip()
            country = ' '.join(country.split()) # несколько пробелов заменяются одним
            year = request.POST.get('year', '').replace(' ', '')
            genre = request.POST.get('genre', '').strip()
            genre = ' '.join(genre.split()) # несколько пробелов заменяются одним
            duration = request.POST.get('duration', '').replace(' ', '')
            producer = request.POST.get('producer', '').strip()
            producer = ' '.join(producer.split()) # несколько пробелов заменяются одним
            actors = request.POST.get('actors', '').strip()
            actors = ' '.join(actors.split()) # несколько пробелов заменяются одним
            video = save_file(request.FILES['video'], 'video')
        except:
            return render(request, 'html/Error.html', {'error': 'Неверный ввод!'})

        if 'id' in request.session:
            user_id = request.session.get('id')
            user = User.objects.get(id = user_id)

            if user.role == 'admin':
                if name and image and about and country and year and genre and duration and producer and actors and video:
                    try:
                        film = Film.objects.filter(name = name)

                        if len(film):
                            return render(request, 'html/Error.html', {'error': 'Фильм уже был добавлен!'})

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
