from django.urls import path
from . import views


urlpatterns = [
    path('', views.ticketing_index, name="ticketing_index"),
    path('ticket_detail/<int:pk>/', views.ticket_detail, name="ticket_detail")
]