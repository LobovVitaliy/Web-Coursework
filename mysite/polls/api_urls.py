from django.conf.urls import url
from . import api_views

urlpatterns = [
    url(r'^signup$', api_views.signup, name = 'signup'),
    url(r'^login$', api_views.login, name = 'login'),
    url(r'^logout$', api_views.logout, name = 'logout'),
    #url(r'^restore$', api_views.restore, name = 'restore'), # востановление
    url(r'^films/page/(\d+)$', api_views.films, name = 'films'),
    url(r'^filminfo/([\w ]+)$', api_views.filminfo, name = 'filminfo'),

    #url(r'^rating$', api_views.rating, name = 'rating'),
    url(r'^add$', api_views.add, name = 'add'),
    #url(r'^sort$', api_views.sort, name = 'sort'),

    url(r'^myfilms/page/(\d+)$', api_views.myfilms, name = 'myfilms'),

    url(r'^addfilm$', api_views.addfilm, name = 'addfilm'),

    url(r'^', api_views.error, name = "error")
]
