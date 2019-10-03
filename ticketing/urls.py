from django.urls import path
from . import views


urlpatterns = [
    path("", views.ticketing_index, name="ticketing_index"),
    path("ticket_detail/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("accounts/register/", views.register, name="register"),
    path("new_ticket/", views.new_ticket, name="new_ticket"),
    path('upload/csv', views.upload_csv, name='upload_csv'),
]
