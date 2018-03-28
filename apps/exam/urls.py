from django.shortcuts import render, redirect
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^loading$', views.loading),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]