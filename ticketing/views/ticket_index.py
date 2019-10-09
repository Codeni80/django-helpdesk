from ticketing.models import Ticket, Category, Status, TicketTable, CustomUser
from ticketing.forms import CustomUserCreationForm, TicketForm, EditTicketForm, FilterBy
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
    current_user = request.user
    user = get_user_model()
    print("STATIC DIRS: {}".format(STATICFILES_DIRS), file=sys.stderr)

    # Checking for sort type, setting it if we can
    if not current_user.u_sort_type:
        current_user.u_sort_type = "-pk"
        current_user.save()  # Setting default sort to sort newest to oldest tickets
    try:
        # Try to set the sort type to what is requested by user
        current_user.u_sort_type = request.GET["sort"]
        current_user.save()
        print("WE SAVED THE SORT TYPE", file=sys.stderr)
    except:
        print("WE HAD AN ERROR SAVING THE SORT TYPE", file=sys.stderr)

    sort_by = current_user.u_sort_type
    print("Sorting by: {0}".format(sort_by), file=sys.stderr)

    # Checking to see if logged in user is a technician (u_permission_level 2),
    # or if they are a user (u_permission_level 1)
    if current_user.u_permission_level == "2":
        if sort_by == 't_subject' or sort_by == '-t_subject':
            if sort_by[0] == "-":
                sort_by = sort_by[1:]
                queryset = Ticket.objects.annotate(
                    t_subject_lower=Lower("t_subject")
                ).order_by(Lower(sort_by).desc())
            else:
                queryset = Ticket.objects.annotate(
                    t_subject_lower=Lower("t_subject")
                ).order_by(Lower(sort_by).asc())
        else:
            queryset = Ticket.objects.all().order_by(sort_by)

        table = TicketTable(queryset)
        RequestConfig(request).configure(table)

        return render(request, "ticketing_index.html", {"table": table})
    else:
        # Non-technicians only see tickets made by/for them.
        if sort_by == 't_subject' or sort_by == '-t_subject':
            if sort_by[0] == "-":
                sort_by = sort_by[1:]
                queryset = Ticket.objects.filter(
                    c_info__username=current_user.username
                ).annotate(t_subject_lower=Lower("t_subject")).order_by(Lower(sort_by).desc())
            else:
                queryset = Ticket.objects.filter(
                    c_info__username=current_user.username
                ).annotate(t_subject_lower=Lower("t_subject")).order_by(Lower(sort_by).asc())
        else:
            queryset = Ticket.objects.filter(
                c_info__username=current_user.username
            ).order_by(sort_by)

        table = TicketTable(queryset)
        RequestConfig(request, paginate={"per_page": 20}).configure(table)

        return render(request, "ticketing_index.html", {"table": table})

def category_helper(sort_by, filter_by):
    pass

def status_helper(sort_by, filter_by):
    pass

def all_ticket_helper(sort_by, filter_by):
    pass

def assigned_ticket_helper(sort_by, filter_by):
    pass

def active_tickets_helper(sort_by, filter_by):
    pass

def closed_tickets_helper(sort_by, filter_by):
    pass

def unasigned_tickets_helper(sort_by, filter_by):
    pass
