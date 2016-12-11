from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name = "home"),
    url(r'^profile$', views.profile, name = 'profile'),

    url(r'^signup$', views.signup, name = 'signup'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),

    url(r'^films/page/(\d+)$', views.films, name = 'films'),
    url(r'^filminfo/([\w.,! -]+)$', views.filminfo, name = 'filminfo'),

    url(r'^myfilms/page/(\d+)$', views.myfilms, name = 'myfilms'),
    url(r'^myfilminfo/([\w.,! -]+)$', views.myfilminfo, name = 'myfilminfo'),
    url(r'^sorted/page/(\d+)$', views.sort, name = 'sort'),

    url(r'^add$', views.add, name = 'add'),
    url(r'^delete$', views.delete, name = 'delete'),
    url(r'^rating$', views.rating, name = 'rating'),
    url(r'^delmyfilms$', views.delmyfilms, name = 'delmyfilms'),

    # Admin
    url(r'^addfilm$', views.addfilm, name = 'addfilm'),

    url(r'^', views.error, name = "error")
]
