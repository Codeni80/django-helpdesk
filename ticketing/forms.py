from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Ticket, Category, Status
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
    def __init__(self, *args, **kwargs):
        self.t_choices = kwargs.pop('t_choices')
        super(TicketForm,self).__init__(*args, **kwargs)
        self.fields['t_assigned'] = forms.ChoiceField(choices=self.t_choices, required=True, label="Assigned To")

    class Meta:
        model = Ticket
        fields = ('t_status', 't_subject', 't_body', 't_category', 'c_info', 't_assigned')