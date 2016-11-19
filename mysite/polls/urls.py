from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name = "home"),
    url(r'^home$', views.home, name = 'home'), # возможно убрать заменить все шаблоны

    url(r'^signup$', views.signup, name = 'signup'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),
    #url(r'^restore$', views.restore, name = 'restore'), # востановление
    url(r'^films/page/(\d+)$', views.films, name = 'films'),
    url(r'^filminfo/([\w ]+)$', views.filminfo, name = 'filminfo'),

    #url(r'^rating$', views.rating, name = 'rating'),
    url(r'^add$', views.add, name = 'add'),
    #url(r'^sort$', views.sort, name = 'sort'),

    url(r'^myfilms/page/(\d+)$', views.myfilms, name = 'myfilms'),

    url(r'^addfilm$', views.addfilm, name = 'addfilm'),

    url(r'^', views.error, name = "error")
]
