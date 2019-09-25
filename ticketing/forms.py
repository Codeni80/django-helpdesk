from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Ticket, Technician, Customer, Category, Status
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import sys

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('u_name', 'username', 'u_phone', 'email', 'u_permission_level')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('u_name', 'username', 'u_phone', 'email', 'u_permission_level')

class TicketForm(forms.ModelForm):
    # choices = [(0, '---------')]

    # user = get_user_model()
    # user = user.objects.filter(u_permission_level=2)
    # i = 1
    
    # for u in user:
    #     choices.append((i, u))
    #     i += 1

    # t_assigned = forms.ChoiceField(choices=choices, required=True, label="Assigned To")

    class Meta:
        model = Ticket
        fields = ('t_status', 't_subject', 't_body', 't_category', 'c_info', 't_assigned')