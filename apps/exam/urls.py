from django.shortcuts import render, redirect
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^loading$', views.loading),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^users/create$', views.create),
    url(r'^users/(?P<id>\d+)$', views.quote),
    url(r'^users/(?P<id>\d+)/delete$', views.delete),
    url(r'^users/(?P<id>\d+)/add$', views.add),
    url(r'^users/(?P<id>\d+)/remove$', views.remove)
]

#     url(r'^users/create$', views.create),
#     url(r'^users/(?P<id>\d+)$', views.quote),
#     url(r'^users/(?P<id>\d+)/delete$', views.delete),
#     url(r'^users/(?P<id>\d+)/add$', views.add),
#     url(r'^users/(?P<id>\d+)/remove$', views.remove),