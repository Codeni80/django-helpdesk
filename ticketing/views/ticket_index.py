from ticketing.models import Ticket, Category, Status, TicketTable, CustomUser
from ticketing.forms import (
    FilterForm,
    CustomUserCreationForm,
    TicketForm,
    EditTicketForm,
    CommentForm
)
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django_tables2 import RequestConfig
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.utils import timezone
from django.db.models.functions import Lower
import sys
from helpdesk.settings import STATICFILES_DIRS


@login_required
def ticketing_index(request):
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        categories = []
        statuses = []
        for stat in Status.objects.all():
            statuses.append(stat.name)
        for cat in Category.objects.all():
            categories.append(cat.name)
        current_user = request.user
        user = get_user_model()

        # Checking for sort type, setting it if we can
        if not current_user.u_sort_type:
            current_user.u_sort_type = "-pk"
            current_user.save()  # Setting default sort to sort newest to oldest tickets
        try:
            # Try to set the sort type to what is requested by user
            current_user.u_sort_type = request.GET["sort"]
        except:
            pass
        try:
            if request.GET["filter"] == "None":
                current_user.u_filter_type = None
            else:
                print("WE SEE FILTER....", file=sys.stderr)
                current_user.u_filter_type = request.GET["filter"]

        except:
            pass
        current_user.save()
        filter_by = current_user.u_filter_type

        sort_by = current_user.u_sort_type
        print("Sorting by: {0}".format(sort_by), file=sys.stderr)
        print("Filtering by: {}".format(filter_by), file=sys.stderr)
        if current_user.u_filter_type is None:
            queryset = all_ticket_helper(
                current_user, current_user.u_permission_level, sort_by, None
            )
        elif current_user.u_filter_type in categories:
            queryset = category_helper(
                current_user,
                current_user.u_permission_level,
                sort_by,
                current_user.u_filter_type,
            )
        elif current_user.u_filter_type in statuses:
            queryset = status_helper(
                current_user,
                current_user.u_permission_level,
                sort_by,
                current_user.u_filter_type,
            )
        elif current_user.u_filter_type == "assigned":
            queryset = assigned_ticket_helper(
                current_user,
                current_user.u_permission_level,
                sort_by,
                user.u_filter_type,
            )
        elif current_user.u_filter_type == "active":
            queryset = active_tickets_helper(
                current_user,
                current_user.u_permission_level,
                sort_by,
                user.u_filter_type,
            )
        elif current_user.u_filter_type == "unassigned":
            queryset = unassigned_tickets_helper(
                current_user,
                current_user.u_permission_level,
                sort_by,
                user.u_filter_type,
            )
        else:
            queryset = Ticket.objects.filter(c_info=None)
        table = TicketTable(queryset)
        RequestConfig(request).configure(table)
        form = FilterForm(
            u_permission_level=current_user.u_permission_level, filter_by=filter_by
        )
        return render(request, "ticketing_index.html", {"table": table, "form": form})


def category_helper(current_user, perms, sort_by, filter_by):
    if perms == "2":
        queryset = Ticket.objects.filter(t_category__name__contains=filter_by).order_by(sort_by)
    else:
        # Non-technicians only see tickets made by/for them.
        queryset = Ticket.objects.filter(
            c_info__username=current_user.username,
            t_category__name__contains=filter_by
        ).order_by(sort_by)
    return queryset


def status_helper(current_user, perms, sort_by, filter_by):
    if perms == "2":
        queryset = Ticket.objects.filter(t_status__name__contains=filter_by).order_by(sort_by)
    else:
        # Non-technicians only see tickets made by/for them.
        queryset = Ticket.objects.filter(
            c_info__username=current_user.username,
            t_status__name__contains=filter_by
        ).order_by(sort_by)
    return queryset


def all_ticket_helper(current_user, perms, sort_by, filter_by):
    if perms == "2":
        queryset = Ticket.objects.all().order_by(sort_by)
    else:
        # Non-technicians only see tickets made by/for them.
        queryset = Ticket.objects.filter(
            c_info__username=current_user.username
        ).order_by(sort_by)
    return queryset


def assigned_ticket_helper(current_user, perms, sort_by, filter_by):
    if perms == "2":
        queryset = Ticket.objects.filter(t_assigned__username__contains=current_user.username).exclude(t_status__name__contains='Closed').order_by(sort_by)
        return queryset
    else:
        queryset = all_ticket_helper(
            current_user, current_user.u_permission_level, sort_by, None
        )
        return queryset


def active_tickets_helper(current_user, perms, sort_by, filter_by):
    if perms == "2":
        queryset = Ticket.objects.all().exclude(t_status__name__contains='Closed').order_by(sort_by)
    else:
        # Non-technicians only see tickets made by/for them.
        queryset = Ticket.objects.filter(
            c_info__username=current_user.username
        ).exclude(t_status__name__contains='Closed').order_by(sort_by)
    return queryset


def unassigned_tickets_helper(current_user, perms, sort_by, filter_by):
    if perms == "2":
        queryset = Ticket.objects.filter(t_assigned__username__isnull=True).order_by(sort_by)
        return queryset
    else:
        queryset = all_ticket_helper(
            current_user, current_user.u_permission_level, sort_by, None
        )
        return queryset
