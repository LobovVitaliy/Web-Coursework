from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings

from polls.models import User, Film
import math, hashlib, datetime, os, json

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

# Create your views here.

def error(request):
    return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')

def signup(request):
    if request.method == 'POST':
        name = ' '.join(request.POST.get('name', '').strip().split())
        mail = request.POST.get('mail', '').replace(' ', '')
        password_1 = request.POST.get('password_1', '').replace(' ', '')
        password_2 = request.POST.get('password_2', '').replace(' ', '')

        if name and mail and password_1 and password_2:
            if password_1 == password_2:
                try:
                    password = make_password(password_1)
                    User.objects.create(name = name, mail = mail, password = password)

                    return HttpResponse(json.dumps({'Success': 'Registration completed successfully'}), content_type = 'application/json')
                except NotUniqueError:
                    return HttpResponse(json.dumps({'Error': 'Mail уже существует!'}), content_type = 'application/json')
                except ValidationError:
                    return HttpResponse(json.dumps({'Error': 'Некорректный ввод mail!'}), content_type = 'application/json')
                except:
                    return HttpResponse(json.dumps({'Error': 'Неизвестная ошибка!'}), content_type = 'application/json')
            else:
                return HttpResponse(json.dumps({'Error': 'Пароли не совпадают!'}), content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({'Error': '400 Bad Request!'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

def login(request):
    if request.method == 'POST':
        mail = request.POST.get('mail', '').replace(' ', '')
        password = request.POST.get('password', '').replace(' ', '')

        if mail and password:
            try:
                user = User.objects.get(mail = mail)
                if check_password(user.password, password):
                    request.session['id'] = str(user.id)
                    return HttpResponse(json.dumps({'Success': 'Login completed successfully'}), content_type = 'application/json')
                else:
                    return HttpResponse(json.dumps({'Error': 'Неверный пароль!'}), content_type = 'application/json')
            except:
                return HttpResponse(json.dumps({'Error': 'Неверный mail!'}), content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({'Error': '400 Bad Request!'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

def logout(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return HttpResponse(json.dumps({'Success': 'Logout completed successfully'}), content_type = 'application/json')

def films(request, page_number):
    if request.method == 'GET':
        value = ' '.join(request.GET.get('value', '').strip().split())

        beg = count_films_on_page * (int(page_number) - 1)
        end = beg + count_films_on_page

        if not value:
            films = Film.objects.all()[beg:end]
        else:
            films = Film.objects.filter(name__icontains = value)[beg:end]

        for film in films:
            f = film.__dict__['_data']
            f.update({'id': str(f['id'])})

        return HttpResponse(json.dumps([f.__dict__['_data'] for f in films]), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

def filminfo(request, name):
    if request.method == 'GET':
        try:
            film = Film.objects.get(name = name)
            f = film.__dict__['_data']
            f.update({'id': str(f['id'])})

            return HttpResponse(json.dumps(film.__dict__['_data']), content_type = 'application/json')
        except:
            return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

def myfilms(request, page_number):
    if request.method == 'GET':
        if 'id' in request.session:
            value = ' '.join(request.GET.get('value', '').strip().split())

            try:
                user_id = request.session.get('id')
                user = User.objects.get(id = user_id)

                for film in user.films:
                    try:
                        f = Film.objects.get(id = film['film'].id)
                    except:
                        user.update(pull__films__id = film['id'])
                        user.update(set__count = user.count - 1)

                user = User.objects.get(id = user_id)

                beg = count_films_on_page * (int(page_number) - 1)
                end = beg + count_films_on_page

                if not value:
                    films = user.films[beg:end]
                else:
                    films = list(filter(lambda film: film['film'].name.lower().find(value.lower()) != -1, user.films))[beg:end]

                for film in films:
                    f = Film.objects.get(id = film['film'].id)

                    for k in f.__dict__['_data'].keys():
                        if k is not 'id':
                            film.update({k: f.__dict__['_data'].setdefault(k)})
                        else:
                            film.update({'id': str(f['id'])})

                    film.update({'date': str(film['date'])})
                    film.pop('film')

                return HttpResponse(json.dumps([f for f in films]), content_type = 'application/json')
            except:
                return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({'Error': '401 Unauthorized!'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

def myfilminfo(request, name):
    if request.method == 'GET':
        if 'id' in request.session:
            try:
                user_id = request.session.get('id')
                user = User.objects.get(id = user_id)

                film = Film.objects.get(name = name)

                for f in user.films:
                    if film.id == f['id']:
                        for k in film.__dict__['_data'].keys():
                            if k is not 'id':
                                f.update({k: film.__dict__['_data'].setdefault(k)})
                            else:
                                f.update({'id': str(film.id)})

                        f.update({'date': str(f['date'])})
                        f.pop('film')
                        return HttpResponse(json.dumps(f), content_type = 'application/json')

                return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')
            except:
                return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({'Error': '401 Unauthorized!'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

def sort(request, page_number):
    if request.method == 'GET':
        if 'id' in request.session:
            value = ' '.join(request.GET.get('value', '').strip().split())

            if value == 'grade' or value == 'date':
                try:
                    user_id = request.session.get('id')
                    user = User.objects.get(id = user_id)

                    for film in user.films:
                        try:
                            f = Film.objects.get(id = film['film'].id)
                        except:
                            user.update(pull__films__id = film['id'])
                            user.update(set__count = user.count - 1)

                    user = User.objects.get(id = user_id)

                    films = user.films

                    beg = count_films_on_page * (int(page_number) - 1)
                    end = beg + count_films_on_page

                    films.sort(key = lambda x: x[value], reverse = True)
                    films = films[beg:end]

                    for f in films:
                        film = Film.objects.get(id = f['id'])

                        for k in film.__dict__['_data'].keys():
                            if k is not 'id':
                                f.update({k: film.__dict__['_data'].setdefault(k)})
                            else:
                                f.update({'id': str(film.id)})

                        f.update({'date': str(f['date'])})
                        f.pop('film')

                    return HttpResponse(json.dumps([f for f in films]), content_type = 'application/json')
                except:
                    return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')
            else:
                return HttpResponse(json.dumps({'Error': '400 Bad Request!'}), content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({'Error': '401 Unauthorized!'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

def addfilm(request):
    if request.method == 'POST':
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
                return HttpResponse(json.dumps({'Error': 'Неверный ввод!'}), content_type = 'application/json')

            user_id = request.session.get('id')
            user = User.objects.get(id = user_id)

            if user.role == 'admin':
                if name and image and about and country and year and genre and duration and producer and actors and video and \
                    re.match(r"^[\w.,! -]+$", name) and re.match(r"^\d{4}$", year) and re.match(r"^\d{2}:\d{2}:\d{2}$", duration):

                    try:
                        film = Film.objects.filter(name = name)
                        if len(film):
                            return HttpResponse(json.dumps({'Error': 'Фильм уже был добавлен!'}), content_type = 'application/json')

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

                        return HttpResponse(json.dumps({'Success': 'Successfully added'}), content_type = 'application/json')
                    except:
                        return HttpResponse(json.dumps({'Error': 'Неверный ввод!'}), content_type = 'application/json')
                else:
                    return HttpResponse(json.dumps({'Error': '400 Bad Request!'}), content_type = 'application/json')
            else:
                return HttpResponse(json.dumps({'Error': '403 Forbidden!'}), content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({'Error': '401 Unauthorized!'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')
