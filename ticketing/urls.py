from django.urls import path
from . import views


urlpatterns = [
    path("", views.ticketing_index, name="ticketing_index"),
    path("ticket_detail/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("accounts/register/", views.register, name="register"),
    path("new_ticket/", views.new_ticket, name="new_ticket"),
    path("upload/csv", views.upload_csv, name="upload_csv"),
    path("accounts/edit_user", views.user_search, name="edit_user"),
    path("accounts/edit_user/<int:pk>/", views.reset_password, name="reset_password"),
    path("accounts/search_results/", views.search_results, name="search_results"),
    path("accounts/change_password", views.change_password, name="change_password"),
    path("accounts/edit_user/update/<int:pk>/", views.update_user, name="update_user")
]
