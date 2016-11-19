from django.db import models
from mongoengine import *

# Create your models here.

class Film(Document):
    meta = {'collection': 'films'}

    name = StringField(required = True, unique = True)
    image = StringField(required = True)
    about = StringField(required = True)
    country = StringField(required = True)
    year = StringField(required = True, max_length = 4)
    genre = StringField(required = True)
    duration = StringField(required = True)
    producer = StringField(required = True)
    actors = StringField(required = True)
    video  = StringField(required = True)

class User(Document):
    meta = {'collection': 'users'}

    role = StringField(default = 'user')
    name = StringField(required = True) # пробелы
    mail = EmailField(required = True, unique = True)
    password = StringField(required = True)
    image = StringField()
    gender = StringField()
    about = StringField() # пробелы
    films = ListField(DictField())
