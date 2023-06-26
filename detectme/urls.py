from django.conf.urls import url, include
from django.urls import path

from . import views

urlpatterns = [
    path('detectme/', views.detectme, name="detectme"),
    ]