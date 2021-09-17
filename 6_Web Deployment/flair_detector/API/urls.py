from django.conf.urls import url
from django.contrib import admin
from API import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^statistics/$', views.statistics, name="statistics")
    ]