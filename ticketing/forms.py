from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import sys


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != "":
                self.fields[field].widget.attrs.update(
                    {
                        "class": "has-popover",
                        "data-content": help_text,
                        "data-placement": "right",
                        "data-container": "body",
                    }
                )
    class Meta:
        model = CustomUser
        fields = ('u_name', 'username', 'u_phone', 'email', 'u_permission_level', 'is_superuser', 'is_staff')


class CustomUserChangeForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        self.u_name = kwargs.pop('u_name')
        self.username = kwargs.pop('username')
        self.u_phone = kwargs.pop('u_phone')
        self.email = kwargs.pop('email')
        self.u_permission_level = kwargs.pop('u_permission_level')
        self.is_superuser = kwargs.pop('is_superuser')
        self.is_staff = kwargs.pop('is_staff')
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['u_name'].initial = self.u_name
        self.fields['username'].initial = self.username
        self.fields['u_phone'].initial = self.u_phone
        self.fields['email'].initial = self.email
        self.fields['u_permission_level'].initial = self.u_permission_level
        self.fields['is_superuser'].initial = self.is_superuser
        self.fields['is_staff'].initial = self.is_staff

    class Meta:
        model = CustomUser
        fields = (
            'u_name',
            'username',
            'u_phone',
            'email',
            'u_permission_level',
            'is_superuser',
            'is_staff',
        )


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.customuser_query = CustomUser.objects.all()
        self.status_query = Status.objects.all()
        self.perm_level = kwargs.pop('perm_level')
        self.u_name = kwargs.pop('u_name')
        self.t_choices = kwargs.pop('t_choices')
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['t_assigned'].queryset = self.t_choices
        self.fields['t_assigned'].initial = None
        self.fields['c_info'] = forms.ModelChoiceField(queryset=self.customuser_query, required=True, initial=None)
        self.fields['t_status'] = forms.ModelChoiceField(queryset=self.status_query)

        if int(self.perm_level) == 1:
            self.fields['c_info'].initial = self.u_name
            self.fields['c_info'].widget = forms.HiddenInput()
            self.fields['t_assigned'].widget = forms.HiddenInput()
            self.fields['t_assigned'].required = False
        
        self.fields["t_status"].widget.attrs["style"] = "width:400px;"
        self.fields["t_subject"].widget.attrs["style"] = "width:400px;"
        # self.fields["t_category"].widget.attrs["style"] = "width:400px;"
        self.fields["c_info"].widget.attrs["style"] = "width:400px;"
        self.fields["t_assigned"].widget.attrs["style"] = "width:400px;"

    class Meta:
        model = Ticket
        fields = (
            't_status',
            't_subject',
            'c_info',
            't_assigned',
        )

class EditTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.status_query = Status.objects.all()
        self.category_query = Category.objects.all()
        self.tech_group = get_user_model()
        self.assigned_query = self.tech_group.objects.filter(u_permission_level=2)
        self.t_status = kwargs.pop('t_status')
        self.t_subject = kwargs.pop('t_subject')
        self.t_category = kwargs.pop('t_category')
        self.t_assigned = kwargs.pop('updating_t_info')
        self.perm_level = kwargs.pop('perm_level')
        super(EditTicketForm, self).__init__(*args, **kwargs)
        self.fields['t_status'] = forms.ModelChoiceField(queryset=self.status_query, initial=self.t_status)
        self.fields['t_subject'] = forms.CharField(initial=self.t_subject)
        self.fields['t_category'] = forms.ModelChoiceField(queryset=self.category_query, initial=self.t_category)
        self.fields['t_assigned'] = forms.ModelChoiceField(queryset=self.assigned_query, initial=self.t_assigned)
        
        self.fields["t_assigned"].widget.attrs["style"] = "width:400px;"
        self.fields["t_status"].widget.attrs["style"] = "width:400px;"
        self.fields["t_subject"].widget.attrs["style"] = "width:400px;"
        self.fields["t_category"].widget.attrs["style"] = "width:400px;"

        if int(self.perm_level) == 1:
            self.fields['t_assigned'].widget = forms.HiddenInput()
            self.fields['t_assigned'].required = False
        

    class Meta:
        model = Ticket
        fields = ('t_status', 't_subject', 't_category', 't_assigned')


class EquipRoomForm(forms.ModelForm):
    queryset = Rooms.objects.all()
    customers = CustomUser.objects.all()

    room = forms.ModelChoiceField(queryset=queryset)
    date = forms.TextInput()
    start_time = forms.TextInput()
    end_time = forms.TextInput()
    t_body = forms.TextInput()

    class Meta:
        model = EquipmentSetup
        fields = ('room', 'date', 'start_time', 'end_time', 't_body')


class EditEquipRoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.e_room = kwargs.pop('room')
        self.e_date = kwargs.pop('date')
        self.e_start_time = kwargs.pop('start_time')
        self.e_end_time = kwargs.pop('end_time')
        self.e_t_body = kwargs.pop('t_body')
        super(EditEquipRoomForm, self).__init__(*args, **kwargs)
        self.default_rm = Rooms.objects.get(room=self.e_room)
        self.queryset = Rooms.objects.all()
        self.fields['room'].queryset = self.queryset
        self.fields['room'].initial = self.default_rm
        self.fields['date'].initial = self.e_date
        self.fields['start_time'].initial = self.e_start_time
        self.fields['end_time'].initial = self.e_end_time
        self.fields['t_body'].initial = self.e_t_body

    class Meta:
        model = EquipmentSetup
        fields = ('room', 'date', 'start_time', 'end_time', 't_body')


class LaptopCheckoutForm(forms.ModelForm):
    reason = forms.CharField(max_length=255)
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    l_body = forms.TextInput()

    class Meta:
        model = LaptopCheckout
        fields = ('reason', 'start_time', 'end_time', 'l_body')


class EditLaptopCheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.reason = kwargs.pop('reason')
        self.start_time = kwargs.pop('start_time')
        self.end_time = kwargs.pop('end_time')
        self.l_body = kwargs.pop('l_body')
        super(EditLaptopCheckoutForm, self).__init__(*args, **kwargs)
        self.fields['reason'].initial = self.reason
        self.fields['start_time'].initial = self.start_time
        self.fields['end_time'].initial = self.end_time
        self.fields['l_body'].initial = self.l_body

    class Meta:
        model = LaptopCheckout
        fields = ('reason', 'start_time', 'end_time', 'l_body')

    
class PrintersForm(forms.ModelForm):
    problem = forms.CharField(max_length=255)
    printer = forms.CharField(max_length=255)
    p_body = forms.TextInput()

    class Meta:
        model = Printers
        fields = ('problem', 'printer', 'p_body')


class EditPrintersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.problem = kwargs.pop('problem')
        self.printer = kwargs.pop('printer')
        self.p_body = kwargs.pop('p_body')
        super(EditPrintersForm, self).__init__(*args, **kwargs)
        self.fields['problem'].initial = self.problem
        self.fields['printer'].initial = self.printer
        self.fields['p_body'].initial = self.p_body

    class Meta:
        model = Printers
        fields = ('problem', 'printer', 'p_body')


class NewStaffForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    department = forms.CharField(max_length=255)
    supervisor = forms.CharField(max_length=255)
    empid = forms.CharField(max_length=255)
    start_date = forms.DateField()
    ns_body = forms.TextInput()

    class Meta:
        model = NewStaff
        fields = ('name', 'department', 'supervisor', 'empid', 'start_date', 'ns_body')


class EditNewStaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        self.department = kwargs.pop('department')
        self.supervisor = kwargs.pop('supervisor')
        self.empid = kwargs.pop('empid')
        self.start_date = kwargs.pop('start_date')
        self.ns_body = kwargs.pop('ns_body')
        super(EditNewStaffForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = self.name
        self.fields['department'].initial = self.department
        self.fields['supervisor'].initial = self.supervisor
        self.fields['empid'].initial = self.empid
        self.fields['start_date'].initial = self.start_date
        self.fields['ns_body'].initial = self.ns_body

    class Meta:
        model = NewStaff
        fields = ('name', 'department', 'supervisor', 'empid', 'start_date', 'ns_body')


class TrainingForm(forms.ModelForm):
    type_query = TrainingType.objects.all()
    location_query = TrainingLoc.objects.all()

    training_type = forms.ModelChoiceField(queryset=type_query)
    staff_name = forms.CharField(max_length=255)
    location = forms.ModelChoiceField(queryset=location_query)
    date = forms.DateTimeField()
    tr_body = forms.TextInput()

    class Meta:
        model = Training
        fields = ('training_type', 'staff_name', 'location', 'date', 'tr_body')


class EditTrainingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.training_type = kwargs.pop('training_type')
        self.staff_name = kwargs.pop('staff_name')
        self.location = kwargs.pop('location')
        self.date = kwargs.pop('date')
        self.tr_body = kwargs.pop('tr_body')
        super(EditTrainingForm, self).__init__(*args, **kwargs)
        self.default_type = TrainingType.objects.get(name=self.training_type)
        self.type_query = TrainingType.objects.all()
        self.default_loc = TrainingLoc.objects.get(locations=self.location)
        self.loc_query = TrainingLoc.objects.all()
        self.fields['training_type'].queryset = self.type_query
        self.fields['training_type'].initial = self.default_type
        self.fields['staff_name'].initial = self.staff_name
        self.fields['location'].queryset = self.loc_query
        self.fields['location'].initial = self.default_loc
        self.fields['date'].initial = self.date
        self.fields['tr_body'].initial = self.tr_body

    class Meta:
        model = Training
        fields = ('training_type', 'staff_name', 'location', 'date', 'tr_body')


class PasswordResetForm(forms.ModelForm):
    account_query = AccountType.objects.all()
    name = forms.CharField(max_length=255)
    account = forms.ModelChoiceField(queryset=account_query)
    pr_body = forms.TextInput()

    class Meta:
        model = PasswordReset
        fields = ('name', 'account', 'pr_body')


class EditPasswordResetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        self.account = kwargs.pop('account')
        self.pr_body = kwargs.pop('pr_body')
        super(EditPasswordResetForm, self).__init__(*args, **kwargs)
        self.default_account = AccountType.objects.get(name=self.account)
        self.account_query = AccountType.objects.all()
        self.fields['name'].initial = self.name
        self.fields['account'].queryset = self.account_query
        self.fields['account'].initial = self.default_account
        self.fields['pr_body'].initial = self.pr_body

    class Meta:
        model = PasswordReset
        fields = ('name', 'account', 'pr_body')


class DefaultTicketForm(forms.ModelForm):
    ticket_body = forms.TextInput()

    class Meta:
        model = DefaultTicket
        fields = ('ticket_body',)


class EditDefaultTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.body = kwargs.pop('ticket_body')
        super(EditDefaultTicketForm, self).__init__(*args, **kwargs)
        self.fields['ticket_body'].initial = self.body

    class Meta:
        model = DefaultTicket
        fields = ('ticket_body',)


class EditUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        ROLE_CHOICES = (('1', 'User'), ('2', 'Technician'))
        self.username = kwargs.pop('username')
        self.u_name = kwargs.pop('u_name')
        self.u_phone = kwargs.pop('u_phone')
        self.email = kwargs.pop('email')
        self.u_permission_level = kwargs.pop('u_permission_level')
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['u_name'].initial = self.u_name
        self.fields['username'].initial = self.username
        self.fields['u_phone'].initial = self.u_phone
        self.fields['email'].initial = self.email
        self.fields['u_permission_level'].initial = self.u_permission_level

    class Meta:
        model = CustomUser
        fields = ('u_name', 'username', 'u_phone', 'email', 'u_permission_level')


class EditUserPasswordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.password = kwargs.pop('password')
        self.username = kwargs.pop('username')
        super(EditUserPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password'].initial = self.username

    class Meta:
        model = CustomUser
        fields = ('password',)


class PasswordChange(forms.Form):
    old_password = forms.CharField(max_length=255, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=255, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput())

    class Meta:
        fields = ('old_password', 'new_password', 'confirm_password')


class CommentForm(forms.ModelForm):
    author = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Update Comment'
        })
    )
    is_private = forms.BooleanField(required=False,
        initial=False,
        label='Private Comment'    
    )

    class Meta:
        model = Comment
        fields = ('body', 'is_private')


class TicketTypeForm(forms.Form):
    category_query = Category.objects.all()

    t_type = forms.ModelChoiceField(queryset=category_query,
        empty_label=None,
        widget=forms.RadioSelect(attrs={'class': 'radioselect'})
    )

    class Meta:
        fields = ('ticket_type')


class UserSearchForm(forms.Form):
    s_filter = forms.CharField(max_length=255, label='Search')

    class Meta:
        fields = 's_filter'


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.perms = kwargs.pop('u_permission_level')
        self.filter_by = kwargs.pop('filter_by')
        super(FilterForm, self).__init__(*args, **kwargs)
        T_CHOICES = [
            ("/?filter=None", "All Tickets"),
            ("/?filter=active", "All Active Tickets"),
            ("/?filter=Closed", "All Closed Tickets"),
            ("/?filter=assigned", "My Assigned Tickets"),
            ("/?filter=unassigned", "All Unassigned Tickets"),
            (" ", "---------------Category Views---------------"),
        ]
        for option in Category.objects.all():
            T_CHOICES.append(
                (
                    "/?filter={}".format(option.name),
                    "All {} Tickets".format(option.name),
                ) 
            )
        T_CHOICES.append(("blank", "-----------------Status Views-----------------"))
        for option in Status.objects.all():
            if option.name != "Closed":
                if option.name != "Open":
                    T_CHOICES.append(
                        (
                            "/?filter={}".format(option.name),
                            "All {} Tickets".format(option.name),
                        )
                    )
        U_CHOICES = [
            ("/?filter=None", "All Tickets"),
            ("/?filter=active", "All Active Tickets"),
            ("/?filter=Closed", "All Closed Tickets"),
        ]

        if self.perms == '2':
            self.fields['filter'] = forms.ChoiceField(
                choices=T_CHOICES, widget=forms.Select(attrs={'class': 'filter'})
            )
        else:
            self.fields['filter'] = forms.ChoiceField(
                choices=U_CHOICES, widget=forms.Select(attrs={'class': 'filter'})
            )

        self.fields["filter"].initial = (
            "/?filter={}".format(self.filter_by),
            "All {} Tickets".format(self.filter_by),
        )

    class Meta:
        fields = 'filter'
