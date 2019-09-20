from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticketing_index, name="ticketing_index"),
]