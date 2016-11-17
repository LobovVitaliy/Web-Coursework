from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name = "home"),
    url(r'^home$', views.home, name = 'home'), # заменить все шаблоны

    url(r'^signup$', views.signup, name = 'signup'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^restore$', views.restore, name = 'restore'), # востановление
    url(r'^films/page/(\d+)$', views.films, name = 'films'),
    url(r'^filminfo/([\w ]+)$', views.filminfo, name = 'filminfo'),

    url(r'^rating$', views.rating, name = 'rating'),
    url(r'^add$', views.add, name = 'add'),
    url(r'^sort$', views.sort, name = 'sort'),

    url(r'^logout$', views.logout, name = 'logout'),

    url(r'^a$', views.a, name = 'a'),
    url(r'^b$', views.b, name = 'b'),

    url(r'^addfilm$', views.addfilm, name = 'addfilm'),

    #url(r'^personal$', views.personal, name = 'personal'),
    #url(r'^myfilms$', views.myfilms, name = 'myfilms'),
    #url(r'^filminfo/(?P<id>\d+)$', views.filminfo, name = 'filminfo'),

    url(r'^index.html$', views.index, name = 'index'),
    url(r'^all.html$', views.all, name = 'all'),
    url(r'^scrum/(?P<id>\d+).html$', views.scrum, name = 'scrum'),

    # lab5:
    url(r'^new.html$', views.new, name = 'new'),
    url(r'^edit/(?P<id>\d+).html$', views.edit, name = 'edit'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = 'delete'),



    url(r'^', views.error, name = "error")
]
