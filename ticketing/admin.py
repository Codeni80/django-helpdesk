from django.contrib import admin
from ticketing.models import Ticket, Category, Status, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm


class TicketAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class StatusAdmin(admin.ModelAdmin):
    pass


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "password",
        "email",
        "u_name",
        "u_phone",
        "u_permission_level",
        "u_sort_type",
        "u_filter_type",
        "force_change",
    ]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
