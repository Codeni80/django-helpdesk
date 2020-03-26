from django.db import models
import django_tables2 as tables
from django_tables2.utils import A
from django.contrib.auth.models import AbstractUser
from django.db.models import F
from django.db.models.functions import Lower
from django.utils import timezone


class Ticket(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    t_opened = models.DateTimeField(auto_now_add=True, verbose_name="Date Opened")
    t_status = models.ForeignKey(
        "Status", on_delete=models.CASCADE, verbose_name="Status"
    )
    t_subject = models.CharField(max_length=100, verbose_name="Subject")
    t_closed = models.DateTimeField(verbose_name="Date Closed", null=True, blank=True)
    t_category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="Category"
    )
    c_info = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Customer Name",
        related_name="customer",
    )
    t_assigned = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Assigned Technician",
        related_name="technician",
        null=True,
        blank=True,
    )
    days_opened = models.TextField(verbose_name="Days Open", 
        null=True, blank=True,
    )

    def __str__(self):
        return self.t_subject


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category")

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name="Status")

    def __str__(self):
        return self.name


class TicketTable(tables.Table):
    pk = tables.LinkColumn(
        "ticket_detail",
        args=[A("pk")],
        verbose_name="Ticket ID",
        attrs={"a": {"style": "color:black"}},
    )
    t_subject = tables.Column(verbose_name="Subject", order_by="t_subject_lower")

    def order_days_open(self, queryset, is_descending):
        queryset = queryset.annotate(
            days_open_sorted = F('t_closed') - F('t_opened')
        )

    def order_t_category(self, queryset, is_descending):
        queryset = queryset.annotate(
            t_category_lower=Lower("t_category__name")
        ).order_by(("-" if is_descending else "") + "t_category_lower")
        return (queryset, True)

    def order_t_status(self, queryset, is_descending):
        queryset = queryset.annotate(
            t_status_lower=Lower("t_status__name")
        ).order_by(("-" if is_descending else "") + "t_status_lower")
        return (queryset, True)

    def order_c_info(self, queryset, is_descending):
        queryset = queryset.annotate(
            c_info_lower=Lower("c_info__u_name")
        ).order_by(("-" if is_descending else "") + "c_info_lower")
        return (queryset, True)

    def order_t_assigned(self, queryset, is_descending):
        queryset = queryset.annotate(
            t_assigned_lower=Lower("t_assigned__u_name")
        ).order_by(("-" if is_descending else "") + "t_assigned_lower")
        return (queryset, True)

    def order_t_subject(self, queryset, is_descending):
        queryset = queryset.annotate(
            t_subject_lower=Lower("t_subject")
        ).order_by(("-" if is_descending else "") + "t_subject_lower")
        return (queryset, True)


    class Meta:
        model = Ticket
        fields = (
            "t_opened",
            "c_info",
            "t_subject",
            "t_status",
            "t_assigned",
            "t_category",
            "t_closed",
            "pk",
            'days_opened'
        )
        template_name = "tables.html"


class CustomUser(AbstractUser):
    ROLE_CHOICES = (("1", "User"), ("2", "Technician"))
    force_change = models.BooleanField(
        verbose_name="Force Password Change on Next Login",
        default=True,
        blank=False,
        null=False,
    )
    u_name = models.CharField(max_length=150, verbose_name="Customer Name")
    u_phone = models.CharField(max_length=14, verbose_name="Customer Phone Number")
    u_permission_level = models.CharField(
        max_length=11, choices=ROLE_CHOICES, verbose_name="Permission Level"
    )
    u_sort_type = models.CharField(
        max_length=30,
        verbose_name="Sort By Value",
        null=True,
        blank=True,
        default="-pk",
    )
    u_filter_type = models.CharField(
        max_length=100,
        verbose_name="Filter By Value",
        null=True,
        blank=True,
        default=None,
    )
    
    def dsl(self):
        dsl = timezone.now() -  self.last_login
        dsl = str(dsl)
        dsl = dsl.split(' ', 1)

        return(dsl[0])

    def __str__(self):
        return self.u_name


class UsersTable(tables.Table):
    update_user = tables.LinkColumn(text='Update User Information',
        viewname='update_user',
        args=[A("pk")],
        verbose_name="Update Information",
        attrs={"a": {"style": "color:grey"}},
        orderable=False,
    )
    change_password = tables.LinkColumn(text='Change User Password',
        viewname='reset_password',
        args=[A("pk")],
        verbose_name="Update Password",
        attrs={"a": {"style": "color:grey"}},
        orderable=False,
    )
    dsl = tables.Column(verbose_name="Days Since Login",
        accessor=A('dsl'),
    )

    def order_dsl(self, queryset, is_descending):
        queryset = queryset.annotate(
            dsl_sort=Lower('last_login')
        ).order_by(("-" if is_descending else "") + "last_login")
        return (queryset, True)

    class Meta:
        model = CustomUser
        fields = ("username", "u_name", "last_login", "dsl", "update_user", "change_password")
        template_name = "tables.html"


class Comment(models.Model):
    author = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, verbose_name="Author"
    )
    body = models.TextField(verbose_name="Body")
    created_on = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE)
    is_private = models.BooleanField(verbose_name="Private Comment", default=False)

class EquipmentSetup(models.Model):
    room = models.ForeignKey("Rooms", on_delete=models.CASCADE)
    date = models.TextField(verbose_name='Date of Event')
    start_time = models.TextField(verbose_name='Time of Event')
    end_time = models.TextField(verbose_name='Approx End of Event')
    t_body = models.TextField(verbose_name='Additional Information (If Any)',
        blank=True,
        null=True,    
    )
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE)


class Rooms(models.Model):
    room = models.CharField(max_length=255)

    def __str__(self):
        return self.room


class LaptopCheckout(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.CharField(verbose_name='Reason', max_length=255)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    l_body = models.TextField(verbose_name='Additional Information (If Any)',
        blank=True,
        null=True,    
    )

class Printers(models.Model):
    problem = models.TextField(verbose_name='Issue With Printer')
    printer = models.CharField(max_length=255)
    p_body = models.TextField(verbose_name='Additional Information (If Any)',
        blank=True,
        null=True,    
    )
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)


class NewStaff(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    department = models.CharField(verbose_name='Department', max_length=255)
    supervisor = models.CharField(verbose_name='Supervisor', max_length=255)
    empid = models.CharField(verbose_name='Employee ID', max_length=255)
    start_date = models.DateTimeField()
    ns_body = models.TextField(verbose_name='Additional Information (If Any)',
        blank=True,
        null=True,    
    )
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)

class Training(models.Model):
    training_type = models.ForeignKey('TrainingType', on_delete=models.CASCADE)
    staff_name = models.CharField(verbose_name='Employee Name', max_length=255)
    location = models.ForeignKey('TrainingLoc', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Proposed Date for Training')
    tr_body = models.TextField(verbose_name='Additional Information (If Any)',
        blank=True,
        null=True,    
    )
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)

class TrainingType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TrainingLoc(models.Model):
    locations = models.CharField(max_length=255)

    def __str__(self):
        return self.locations

class PasswordReset(models.Model):
    name = models.CharField(max_length=255, verbose_name='Staff Name')
    account = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    pr_body = models.TextField(verbose_name='Additional Information (If Any)',
        blank=True,
        null=True,    
    )
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)

class AccountType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class DefaultTicket(models.Model):
    ticket_body = models.TextField(verbose_name='Ticket Summary')
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)


    def __str__(self):
        return self.body
