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

class EditTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self.t_opened = kwargs.pop('t_opened')
        self.t_status = kwargs.pop('t_status')
        self.status_choices = kwargs.pop('status_choices')
        self.t_subject = kwargs.pop('t_subject')
        self.t_body = kwargs.pop('t_body')
        # self.t_closed = kwargs.pop('t_closed')
        self.t_category = kwargs.pop('t_category')
        self.category_choices = kwargs.pop('category_choices')
        super(EditTicketForm, self).__init__(*args, **kwargs)
        self.fields['t_status'].queryset = self.status_choices
        self.fields['t_status'].initial = self.t_status
        self.fields['t_subject'] = forms.CharField(initial=self.t_subject)
        self.fields['t_body'].initial = self.t_body
        # self.fields['t_category'] = forms.ChoiceField(choices=self.category_choices, initial=self.t_category)
        self.fields['t_category'].queryset = self.category_choices
        self.fields['t_category'].initial = self.t_category
        

    class Meta:
        model = Ticket
        fields = ('t_status', 't_subject', 't_body', 't_category')