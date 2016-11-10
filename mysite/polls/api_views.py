from django.http import QueryDict, HttpResponse
from pymongo import MongoClient

import json

# Create your views here.

def all(request):
    if request.method == 'GET':
        client = MongoClient()
        collection = client.lab4.sm

        ScrumMasters = []
        for i in collection.find():
            ScrumMasters.append(i)
            ScrumMasters[len(ScrumMasters) - 1].pop('_id')

        client.close();
        return HttpResponse(json.dumps(ScrumMasters), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

def sort(request, username):
    if request.method == 'GET':
        print (request.GET.get(username))
        client = MongoClient()
        collection = client.lab4.sm

        ScrumMasters = []
        for i in collection.find():
            ScrumMasters.append(i)
            ScrumMasters[len(ScrumMasters) - 1].pop('_id')

        client.close();
        return HttpResponse(json.dumps(ScrumMasters), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

# изменить бд в Delete, Put
# Put: как реагировать на неправильный ключ
def scrum(request, id):
    if request.method == 'GET':
        client = MongoClient()
        collection = client.lab4.sm
        ScrumMaster = collection.find_one({'id': id})
        maxCount = collection.count()
        client.close();

        if int(id) >= 1 and int(id) <= maxCount:
            ScrumMaster.pop('_id')
            return HttpResponse(json.dumps(ScrumMaster), content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')
    elif request.method == 'PUT':
        client = MongoClient()
        collection = client.test.scrum_master   # изменить бд
        ScrumMaster = collection.find_one({'id': id})
        maxCount = collection.count()

        if int(id) >= 1 and int(id) <= maxCount:
            req_body = request.body.decode('utf-8')
            edit = QueryDict(req_body)

            for key in edit.keys():
                if key == 'name' or key == 'surname' or key == 'date' or key == 'count' or key == 'score':
                    collection.update({'id': id}, { "$set": {key: edit[key].replace(' ', '').title()} })
                else:
                    print("err key: " + key)

            client.close();
            return HttpResponse(json.dumps({'Success': 'Successfully updated'}), content_type = 'application/json')
        else:
            client.close();
            return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')
    elif request.method == 'DELETE':
        client = MongoClient()
        collection = client.test.scrum_master   # изменить бд
        ScrumMaster = collection.find_one({'id': id})
        maxCount = collection.count()

        if int(id) >= 1 and int(id) <= maxCount:
            collection.remove({'id': id})

            client.close();
            return HttpResponse(json.dumps({'Success': 'Successfully deleted'}), content_type = 'application/json')
        else:
            client.close();
            return HttpResponse(json.dumps({'Error': '404 Not Found!'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')

# Post: должны ли быть заполены все поля
def new(request):
    if request.method == 'POST':
        req_body = request.body.decode('utf-8')
        new = QueryDict(req_body)

        client = MongoClient()
        collection = client.test.scrum_master

        # checks
        keys = ['name', 'surname', 'date', 'count', 'score']

        if len(new.keys()) != len(keys):
            client.close();
            return HttpResponse(json.dumps({'Error': '400 Bad Request!'}), content_type = 'application/json')

        for key in new.keys():
            for i in range(len(keys)):
                if key == keys[i]:
                    keys.pop(i)
                    break

        if len(keys) != 0:
            client.close();
            return HttpResponse(json.dumps({'Error': '400 Bad Request!'}), content_type = 'application/json')

        if new.get('name').replace(' ', '') and new.get('surname').replace(' ', '') \
        and new.get('date').replace(' ', '') and new.get('count').replace(' ', '') \
        and new.get('score').replace(' ', ''):
            pass
        else:
            client.close();
            return HttpResponse(json.dumps({'Error': '400 Bad Request!'}), content_type = 'application/json')

        # end checks

        collection.insert ({
            'id': str(collection.count() + 1),
            'name': new['name'].title(),
            'surname': new['surname'].title(),
            'date': new['date'],
            'count': new['count'],
            'score': new['score'],
        })

        client.close();
        return HttpResponse(json.dumps({'Success': 'Successfully added'}), content_type = 'application/json')
    else:
        return HttpResponse(json.dumps({'Error': '405 Method Not Allowed!'}), content_type = 'application/json')
