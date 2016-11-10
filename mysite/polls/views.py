from django.shortcuts import render, redirect
from django.http import QueryDict
from pymongo import MongoClient

import random, json

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

def check_signup(body):
    keys = ['name', 'mail', 'password_1', 'password_2']

    if not check_keys(body, keys):
        pass # error

    if len(body['name']) > 20:
        pass # error
    if len(body['mail']) > 50:
        pass # error
    if body['mail'].find('@') == -1:
        pass # error
    if body['password_1'] != body['password_2']:
        pass # error

    return True

def check_signin(body):
    keys = ['mail', 'password']

    if not check_keys(body, keys):
        pass # error

    if len(body['mail']) > 50:
        pass # error
    if body['mail'].find('@') == -1:
        pass # error

    return True

# Create your views here.

def home(request):
    if request.method == 'GET':
        client = MongoClient()
        collection = client.mysite.users

        collection.insert ({
            'role': 'admin',
            'name': 'Vitaliy',
            'mail': '1234@gmail.ru',
            'password': '12345',
            'gender': 'man',
            'image': 'none',
            'about': 'none'
        })

        client.close();

        return render(request, 'html/index.html', {})
        #return render(request, 'html/home.html', {})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def signup(request):
    if request.method == 'GET':
        return render(request, 'html/signup.html', {})
    elif request.method == 'POST':
        body = QueryDict(request.body.decode('utf-8'))

        check, error = check_signup(body)

        if check:
            pass # add to bd
        else:
            pass # error

        return render(request, 'html/index.html', {})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def signin(request):
    if request.method == 'GET':
        return render(request, 'html/signin.html', {})
    elif request.method == 'POST':
        body = QueryDict(request.body.decode('utf-8'))

        check, error = check_signin(body)

        if check:
            pass # sign in
        else:
            pass # error

        return render(request, 'html/index.html', {})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def restore(request):
    if request.method == 'GET':
        return render(request, 'html/restore.html', {})
    elif request.method == 'POST':
        pass
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def films(request, page):
    if request.method == 'GET':
        client = MongoClient()
        collection = client.mysite.films

        collection.insert ({
            'name': '',
            'image': '',
            'about': '',
            'country': '',
            'year': '',
            'genre': '',
            'duration': '',
            'producer': '',
            'actors': '',
            'story': '',
            'film': ''
        })

        client.close();

        return render(request, 'html/index.html', {})
        #return render(request, 'html/films.html', {})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})

def filminfo(request, id):
    if request.method == 'GET':
        if int(id) >= 1 and int(id) <= maxCount:
            return render(request, 'html/filminfo.html', {'film': film})
        else:
            return render(request, 'html/Error.html', {'error': '404 Not Found!'})
    else:
        return render(request, 'html/Error.html', {'error': '405 Method Not Allowed!'})






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
