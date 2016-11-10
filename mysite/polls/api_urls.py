from django.conf.urls import url
from . import api_views

urlpatterns = [
    url(r'^all$', api_views.all, name = 'all'),
    url(r'^sort(?P<username>\w+)$', api_views.sort, name = 'sort'),
    url(r'^scrum/(?P<id>\d+)$', api_views.scrum, name = 'scrum'),
    url(r'^new$', api_views.new, name = 'new'),
]
