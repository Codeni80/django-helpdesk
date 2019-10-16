from django.db import models
import django_tables2 as tables
from django_tables2.utils import A
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower


class Ticket(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    t_opened = models.DateTimeField(auto_now_add=True, verbose_name="Date Opened")
    t_status = models.ForeignKey(
        "Status", on_delete=models.CASCADE, verbose_name="Status"
    )
    t_subject = models.CharField(max_length=100, verbose_name="Subject")
    t_body = models.TextField(verbose_name="Ticket Summary")
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
    # t_assigned = models.CharField(max_length=150, verbose_name='Assigned To')
    t_assigned = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Assigned Technician",
        related_name="technician",
        null=True,
        blank=True,
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

    def __str__(self):
        return self.u_name


class UsersTable(tables.Table):
    # pk = tables.LinkColumn(
    #     "update_user",
    #     args=[A("pk")],
    #     verbose_name="Customer ID",
    #     attrs={"a": {"style": "color:black"}},
    # )
    update_user = tables.LinkColumn(text='Update User Information',
        viewname='update_user',
        args=[A("pk")],
        verbose_name="Udate Information",
        attrs={"a": {"style": "color:grey"}},
    )
    change_password = tables.LinkColumn(text='Change Users Password',
        viewname='reset_password',
        args=[A("pk")],
        verbose_name="Udate Information",
        attrs={"a": {"style": "color:grey"}},
    )
    class Meta:
        model = CustomUser
        fields = ("username", "u_name", "last_login", "update_user", "change_password")
        template_name = "tables.html"
