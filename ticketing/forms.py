from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Ticket, Category, Status
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import sys


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("u_name", "username", "u_phone", "email", "u_permission_level")
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['u_name'].widget.attrs.update({'autofocus': 'autofocus'})
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body'})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("u_name", "username", "u_phone", "email", "u_permission_level")


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.t_choices = kwargs.pop("t_choices")
        self.perm_level = kwargs.pop("perm_level")
        self.u_name = kwargs.pop("u_name")
        self.c_choices = kwargs.pop("c_choices")
        # self.t_assigned = kwargs.pop('t_assigned')
        super(TicketForm, self).__init__(*args, **kwargs)
        # self.fields['t_assigned'] = forms.ChoiceField(choices=self.t_choices, required=True, label="Assigned To")
        self.fields["t_assigned"].queryset = self.t_choices
        self.fields["t_assigned"].initial = None
        self.fields["c_info"].queryset = self.c_choices
        
        if int(self.perm_level) == 1:
            self.fields["c_info"].initial = self.u_name
            self.fields["c_info"].widget = forms.HiddenInput()
            self.fields["t_assigned"].widget = forms.HiddenInput()
            self.fields["t_assigned"].required = False

        self.fields["t_status"].widget.attrs['style'] = 'width:400px;'
        self.fields["t_subject"].widget.attrs['style'] = 'width:400px;'
        self.fields["t_body"].widget.attrs['style'] = 'width:400px; height:150px'
        self.fields["t_category"].widget.attrs['style'] = 'width:400px;'
        self.fields["c_info"].widget.attrs['style'] = 'width:400px;'
        self.fields["t_assigned"].widget.attrs['style'] = 'width:400px;'

    class Meta:
        model = Ticket
        fields = (
            "t_status",
            "t_subject",
            "t_body",
            "t_category",
            "c_info",
            "t_assigned",
        )


class EditTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self.t_opened = kwargs.pop('t_opened')
        self.t_status = kwargs.pop("t_status")
        self.status_choices = kwargs.pop("status_choices")
        self.t_subject = kwargs.pop("t_subject")
        self.t_body = kwargs.pop("t_body")
        # self.t_closed = kwargs.pop('t_closed')
        self.t_category = kwargs.pop("t_category")
        self.category_choices = kwargs.pop("category_choices")
        super(EditTicketForm, self).__init__(*args, **kwargs)
        self.fields["t_status"].queryset = self.status_choices
        self.fields["t_status"].initial = self.t_status
        self.fields["t_subject"] = forms.CharField(initial=self.t_subject)
        self.fields["t_body"].initial = self.t_body
        # self.fields['t_category'] = forms.ChoiceField(choices=self.category_choices, initial=self.t_category)
        self.fields["t_category"].queryset = self.category_choices
        self.fields["t_category"].initial = self.t_category

        self.fields["t_status"].widget.attrs['style'] = 'width:400px;'
        self.fields["t_subject"].widget.attrs['style'] = 'width:400px;'
        self.fields["t_body"].widget.attrs['style'] = 'width:400px; height: 150px'
        self.fields["t_category"].widget.attrs['style'] = 'width:400px;'

    class Meta:
        model = Ticket
        fields = ("t_status", "t_subject", "t_body", "t_category")


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.perms = kwargs.pop('u_permission_level')
        self.filter_by = kwargs.pop('filter_by')
        super(FilterForm, self).__init__(*args, **kwargs)
        T_CHOICES = [('/?filter=None', 'All Tickets'),
            ('/?filter=active', 'All Active Tickets'), 
            ('/?filter=Closed', 'All Closed Tickets'), 
            ('/?filter=assigned', "My Assigned Tickets"), 
            (' ', '---------------Category Views---------------')]
        for option in Category.objects.all():
            T_CHOICES.append(("/?filter={}".format(option.name), "All {} Tickets".format(option.name)))
        T_CHOICES.append(('blank', '-----------------Status Views-----------------'))
        for option in Status.objects.all():
            if option.name != "Closed":
                if option.name != "Open":
                    T_CHOICES.append(("/?filter={}".format(option.name), "All {} Tickets".format(option.name)))
        
        U_CHOICES = [('/?None', 'All Tickets'), 
            ('/?active', 'All Active Tickets'), 
            ('/?Closed', 'All Closed Tickets')]

        if self.perms == "2":
            self.fields['filter'] = forms.ChoiceField(choices=T_CHOICES, widget=forms.Select(attrs={'class':'filter'}))
        else:
            self.fields['filter'] = forms.ChoiceField(choices=U_CHOICES)
        try:
            self.fields['filter'].initial = ("/?filter={}".format(self.filter_by), "All {} Tickets".format(self.filter_by))
        except:
            print("error")
    class Meta:
        fields = ("filter")
