from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .mongoengine.errors import NotUniqueError, ValidationError
from django.core.paginator import Paginator
from django.conf import settings

from polls.models import User, Film
import math, hashlib, datetime, os, re, json

count_films_on_page = 4

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

def getArgs(request, args = None, error = None):
    if not args:
        args = {}

    if 'id' in request.session:
        args.update({'registered': True})
    else:
        args.update({'registered': False})

    if error:
        args.update({'error': error})

    return args

# Create your views here.

# session by id ?
# try-except users или можно всего блока ?
# все, что связано с ошибками
    # при ошибках статус (404...) ?
    # правилость написания ошибок
# login, signup: если уже вошли на сайт, то перекидывать на homepage ?

# заменить все  Method Not Allowed! (other) на 1 функцию ?

# return HttpResponse(json.dumps({'data': 'ok'}), content_type = 'application/json')

def error(request):
    if request.method == 'GET':
        args = getArgs(request, error = '404 Not Found!')
        return render(request, 'html/Error.html', args)
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def home(request):
    if request.method == 'GET':
        args = getArgs(request)
        return render(request, 'html/home.html', args)
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def profile(request):
    if request.method == 'GET':
        if 'id' in request.session:
            try:
                user_id = request.session.get('id')
                user = User.objects.get(id = user_id)

                user.__dict__['_data'].pop('id')
                user.__dict__['_data'].pop('password')

                return render(request, 'html/profile.html', {'user': user, 'registered': True})
            except:
                return render(request, 'html/Error.html', {'error': '404 Not Found!'})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def signup(request):
    if request.method == 'GET':
        if 'id' in request.session:
            return redirect('/')
        else:
            return render(request, 'html/signup.html', {})
    elif request.method == 'POST':
        name = ' '.join(request.POST.get('name', '').strip().split())
        mail = request.POST.get('mail', '').replace(' ', '')
        password_1 = request.POST.get('password_1', '').replace(' ', '')
        password_2 = request.POST.get('password_2', '').replace(' ', '')

        if name and mail and password_1 and password_2:
            if password_1 == password_2:
                try:
                    password = make_password(password_1)
                    User.objects.create(name = name, mail = mail, password = password)
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

def login(request):
    if request.method == 'GET':
        if 'id' in request.session:
            return redirect('/')
        else:
            return render(request, 'html/login.html', {})
    elif request.method == 'POST':
        mail = request.POST.get('mail', '').replace(' ', '')
        password = request.POST.get('password', '').replace(' ', '')

        if mail and password:
            try:
                user = User.objects.get(mail = mail)
                if check_password(user.password, password):
                    request.session['id'] = str(user.id)
                    return redirect('/')
                else:
                    return render(request, 'html/Error.html', {'error': 'Неверный пароль!'})
            except:
                return render(request, 'html/Error.html', {'error': 'Неверный mail!'})
        else:
            return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def logout(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return redirect('/')

def search(request):
    if request.method == 'GET':
        value = ' '.join(request.GET.get('value', '').strip().split())

        films = Film.objects.filter(name__icontains = value)
        for f in films:
            a = f.__dict__['_data']
            a.update({'id': str(a['id'])})

        b = json.dumps([f.__dict__['_data'] for f in films])
        return HttpResponse(b, content_type = 'application/json', status = 200)
        return HttpResponse(json.dumps({'data':'3'}), content_type = 'application/json', status = 200)
    else:
        return HttpResponse(json.dumps({'data': '405 Method Not Allowed!'}), content_type = 'application/json', status = 405)

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

            #args = getArgs(request, args)
            args.update({'films': current_page.page(page_number), 'ismyfilms': False})

            return render(request, 'html/films.html', args)
        else:
            #args = getArgs(request, error = '404 Not Found!')
            return render(request, 'html/Error.html', args)
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# name__icontains -> name (? не отправляет как символ)
def filminfo(request, name):
    if request.method == 'GET':
        try:
            film = Film.objects.get(name = name)

            args = getArgs(request)
            args.update({'film': film, 'ismyfilms': False})

            return render(request, 'html/filminfo.html', args)
        except:
            args = getArgs(request, error = '404 Not Found!')
            return render(request, 'html/Error.html', args)
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def myfilms(request, page_number):
    if request.method == 'GET':
        if 'id' in request.session:
            value = ' '.join(request.GET.get('value', '').strip().split())

            try:
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
                    args.update({'films': current_page.page(page_number), 'ismyfilms': True, 'registered': True})
                    return render(request, 'html/films.html', args)
                else:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!', 'registered': True})
            except:
                return render(request, 'html/Error.html', {'error': '404 Not Found!'})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# name__icontains -> name (? не отправляет как символ)
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
                        return render(request, 'html/filminfo.html', {'film': f, 'ismyfilms': True, 'registered': True})

                return render(request, 'html/Error.html', {'error': '404 Not Found!', 'registered': True})
            except:
                return render(request, 'html/Error.html', {'error': '404 Not Found!', 'registered': True})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def sort(request, page_number):
    if request.method == 'GET':
        if 'id' in request.session:
            value = ' '.join(request.GET.get('value', '').strip().split())

            if value == 'grade' or value == 'date':
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    films = user.films

                    films.sort(key = lambda x: x[value], reverse = True)

                    if int(page_number) >= 1 and int(page_number) <= math.ceil(len(films) / count_films_on_page):
                        current_page = Paginator(films, count_films_on_page)

                        args = {
                            'films': current_page.page(page_number),
                            'registered': True,
                            'ismyfilms': True,
                            'sorted': value
                        }

                        return render(request, 'html/films.html', args)
                    else:
                        return render(request, 'html/Error.html', {'error': '404 Not Found!', 'registered': True})
                except:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            else:
                return render(request, 'html/Error.html', {'error': '400 Bad Request!', 'registered': True})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def add(request):
    if request.method == 'POST':
        if 'id' in request.session:
            name = ' '.join(request.POST.get('name', '').strip().split())

            if name:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    film = Film.objects.get(name = name)

                    for f in user.films:
                        if film == f['film']:
                            return HttpResponse(json.dumps({'data': 'Фильм уже был добавлен'}), content_type = 'application/json', status = 200)

                    myfilm = {'film': film, 'grade': 0, 'date': datetime.datetime.now()}
                    user.update(add_to_set__films = myfilm)
                    user.update(set__count = user.count + 1)

                    return HttpResponse(json.dumps({'data': 'Фильм успешно добавлен'}), content_type = 'application/json', status = 200)
                except:
                    return HttpResponse(json.dumps({'data': '404 Not Found!'}), content_type = 'application/json', status = 404)
            else:
                return HttpResponse(json.dumps({'data': '400 Bad Request!'}), content_type = 'application/json', status = 400)
        else:
            return HttpResponse(json.dumps({'data': '401 Unauthorized!'}), content_type = 'application/json', status = 401)
    else:
        return HttpResponse(json.dumps({'data': '405 Method Not Allowed!'}), content_type = 'application/json', status = 405)

# def add(request):
#     if request.method == 'POST':
#         if 'id' in request.session:
#             name = ' '.join(request.POST.get('name', '').strip().split())
#
#             if name:
#                 try:
#                     user_id = request.session.get('id')
#                     user = User.objects.get(id = user_id)
#                     film = Film.objects.get(name = name)
#
#                     for f in user.films:
#                         if film == f['film']:
#                             return render(request, 'html/Error.html', {'error': 'Фильм уже был добавлен!', 'registered': True})
#
#                     myfilm = {'film': film, 'grade': '0', 'date': datetime.datetime.now()}
#                     user.update(add_to_set__films = myfilm)
#                     user.update(set__count = user.count + 1)
#
#                     return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
#                 except:
#                     return render(request, 'html/Error.html', {'error': '404 Not Found!', 'registered': True})
#             else:
#                 return render(request, 'html/Error.html', {'error': '400 Bad Request!', 'registered': True})
#         else:
#             return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
#     else:
#         return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# не всегда удается удалить фильм
def delete(request):
    if request.method == 'POST':
        if 'id' in request.session:
            name = ' '.join(request.POST.get('name', '').strip().split())

            if name:
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    film = Film.objects.get(name = name)

                    for f in user.films:
                        if film == f['film']:
                            user.update(pull__films = f)
                            user.update(set__count = user.count - 1)
                            break

                    return redirect('/myfilms/page/1', {'registered': True})
                except:
                    return render(request, 'html/Error.html', {'error': '404 Not Found!'})
            else:
                return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# не всегда удается установить рейтинг
def rating(request):
    if request.method == 'POST':
        if 'id' in request.session:
            name = ' '.join(request.POST.get('name', '').strip().split())
            grade = request.POST.get('grade', '').replace(' ', '')

            if name and grade and grade.isdigit():
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)
                    film = Film.objects.get(name = name)

                    for f in user.films:
                        if film == f['film']:
                            updated = dict(date = f['date'], film = f['film'], grade = int(grade))
                            user.update(pull__films = f)
                            user = User.objects.get(id = user_id)
                            user.update(add_to_set__films = updated)
                            break

                    return HttpResponse(json.dumps({'data': 'Рейтинг обновлен'}), content_type = 'application/json', status = 200)
                except:
                    return HttpResponse(json.dumps({'data': '404 Not Found'}), content_type = 'application/json', status = 404)
            else:
                return HttpResponse(json.dumps({'data': '400 Bad Request'}), content_type = 'application/json', status = 400)
        else:
            return HttpResponse(json.dumps({'data': '401 Unauthorized'}), content_type = 'application/json', status = 401)
    else:
        return HttpResponse(json.dumps({'data': '405 Method Not Allowed'}), content_type = 'application/json', status = 405)

# def rating(request):
#     if request.method == 'POST':
#         if 'id' in request.session:
#             name = ' '.join(request.POST.get('name', '').strip().split())
#             grade = request.POST.get('grade', '').replace(' ', '')
#
#             if name and grade and grade.isdigit():
#                 try:
#                     user_id = request.session.get('id')
#                     user = User.objects.get(id = user_id)
#                     film = Film.objects.get(name = name)
#
#                     for f in user.films:
#                         if film == f['film']:
#                             updated = dict(date = f['date'], film = f['film'], grade = grade)
#                             user.update(pull__films = f)
#                             user = User.objects.get(id = user_id)
#                             user.update(add_to_set__films = updated)
#                             break
#
#                     return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
#                 except:
#                     return render(request, 'html/Error.html', {'error': '404 Not Found!'})
#             else:
#                 return render(request, 'html/Error.html', {'error': '400 Bad Request!'})
#         else:
#             return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
#     else:
#         return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def delmyfilms(request):
    if request.method == 'POST':
        if 'id' in request.session:
            try:
                user_id = request.session.get('id')
                user = User.objects.get(id = user_id)
                user.update(set__films = [])
                user.update(set__count = 0)

                return HttpResponse(json.dumps({'data': 'Коллекция успешно удалена'}), content_type = 'application/json', status = 200)
            except:
                return HttpResponse(json.dumps({'data': '404 Not Found'}), content_type = 'application/json', status = 404)
        else:
            return HttpResponse(json.dumps({'data': '401 Unauthorized'}), content_type = 'application/json', status = 401)
    else:
        return HttpResponse(json.dumps({'data': '405 Method Not Allowed'}), content_type = 'application/json', status = 405)

# def delmyfilms(request):
#     if request.method == 'POST':
#         if 'id' in request.session:
#             try:
#                 user_id = request.session.get('id')
#                 user = User.objects.get(id = user_id)
#                 user.update(set__films = [])
#                 user.update(set__count = 0)
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
#             except:
#                 return render(request, 'html/Error.html', {'error': '404 Not Found!'})
#         else:
#             return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
#     else:
#         return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

# Admin
def addfilm(request):
    if request.method == 'GET':
        if 'id' in request.session:
            user_id = request.session.get('id')
            user = User.objects.get(id = user_id)

            if user.role == 'admin':
                return render(request, 'html/addfilm.html', {'registered': True})
            else:
                return render(request, 'html/Error.html', {'error': '403 Forbidden!', 'registered': True})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    elif request.method == 'POST':
        if 'id' in request.session:
            try:
                name = ' '.join(request.POST.get('name', '').strip().split())
                image = save_file(request.FILES['image'], 'image')
                about = ' '.join(request.POST.get('about', '').strip().split())
                country = ' '.join(request.POST.get('country', '').strip().split())
                year = request.POST.get('year', '').replace(' ', '')
                genre = ' '.join(request.POST.get('genre', '').strip().split())
                duration = request.POST.get('duration', '').replace(' ', '')
                producer = ' '.join(request.POST.get('producer', '').strip().split())
                actors = ' '.join(request.POST.get('actors', '').strip().split())
                video = save_file(request.FILES['video'], 'video')
            except:
                return render(request, 'html/Error.html', {'error': 'Неверный ввод!'})

            user_id = request.session.get('id')
            user = User.objects.get(id = user_id)

            if user.role == 'admin':
                if name and image and about and country and year and genre and duration and producer and actors and video and \
                    re.match(r"^[\w.,! -]+$", name) and re.match(r"^\d{4}$", year) and re.match(r"^\d{2}:\d{2}:\d{2}$", duration):

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

                        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
                    except:
                        return render(request, 'html/Error.html', {'error': 'Неверный ввод!', 'registered': True})
                else:
                    return render(request, 'html/Error.html', {'error': '400 Bad Request!', 'registered': True})
            else:
                return render(request, 'html/Error.html', {'error': '403 Forbidden!', 'registered': True})
        else:
            return render(request, 'html/Error.html', {'error': '401 Unauthorized!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})
