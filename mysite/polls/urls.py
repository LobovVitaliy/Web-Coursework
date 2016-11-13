from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home$', views.home, name = 'home'),
    url(r'^signup$', views.signup, name = 'signup'),
    url(r'^signin$', views.signin, name = 'signin'),
    url(r'^restore$', views.restore, name = 'restore'), # востановление
    url(r'^films/page/(?P<page_number>\d+)$', views.films, name = 'films'),
    url(r'^filminfo/(?P<id>\d+)$', views.filminfo, name = 'filminfo'),

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
]
