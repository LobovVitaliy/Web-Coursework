# URL Configuration https://docs.djangoproject.com/en/1.10/topics/http/urls/

from django.conf.urls import include, url
#from django.contrib import admin

urlpatterns = [
    url(r'^api/', include('polls.api_urls')),
    url(r'^', include('polls.urls')),
]
