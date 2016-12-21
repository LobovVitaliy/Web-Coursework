from django.conf.urls import url
from . import api_views

urlpatterns = [
    url(r'^signup$', api_views.signup, name = 'signup'),
    url(r'^login$', api_views.login, name = 'login'),
    url(r'^logout$', api_views.logout, name = 'logout'),

    url(r'^films/page/(\d+)$', api_views.films, name = 'films'),
    url(r'^filminfo/([\w.,! -]+)$', api_views.filminfo, name = 'filminfo'),

    url(r'^myfilms/page/(\d+)$', api_views.myfilms, name = 'myfilms'),
    url(r'^myfilminfo/([\w.,! -]+)$', api_views.myfilminfo, name = 'myfilminfo'),
    url(r'^sorted/page/(\d+)$', api_views.sort, name = 'sort'),

    # Admin
    url(r'^addfilm$', api_views.addfilm, name = 'addfilm'),

    url(r'^', api_views.error, name = "error")
]
