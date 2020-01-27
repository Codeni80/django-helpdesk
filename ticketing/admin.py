from django.contrib import admin
from ticketing.models import *
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
        "is_superuser",
        "is_staff"
    ]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Comment)
admin.site.register(Rooms)
admin.site.register(EquipmentSetup)
admin.site.register(LaptopCheckout)
admin.site.register(Printers)
admin.site.register(NewStaff)
admin.site.register(Training)
admin.site.register(TrainingType)
admin.site.register(TrainingLoc)
admin.site.register(PasswordReset)
admin.site.register(AccountType)
admin.site.register(DefaultTicket)

