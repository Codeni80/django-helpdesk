from ticketing.models import Ticket, Category, Status, TicketTable, CustomUser
from ticketing.forms import CustomUserCreationForm, TicketForm, EditTicketForm
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

@login_required
def ticket_detail(request, pk):
    current_user = request.user
    print(current_user.u_permission_level, file=sys.stderr)

    ticket = Ticket.objects.get(pk=pk)
    updating_pk = ticket.pk
    updating_cinfo = ticket.c_info
    updating_tinfo = ticket.t_assigned
    updating_ts = ticket.timestamp
    updating_opened = ticket.t_opened
    status_choices = Status.objects.all()
    t_subject = ticket.t_subject
    t_body = ticket.t_body
    t_status = ticket.t_status

    category_choices = Category.objects.all()

    t_category = ticket.t_category.pk

    context = {"ticket": ticket}
    if request.method == "POST":
        form = EditTicketForm(
            request.POST,
            t_status=t_status,
            status_choices=status_choices,
            t_subject=t_subject,
            t_body=t_body,
            t_category=t_category,
            category_choices=category_choices,
        )
        status = Status.objects.filter(name=form.t_status)
        ticket.status = status
        print("Ticket.status: {0}".format(ticket.status), file=sys.stderr)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.pk = updating_pk
            ticket.status = status
            ticket.c_info = updating_cinfo
            ticket.t_assigned = updating_tinfo
            ticket.timestamp = updating_ts
            ticket.t_opened = updating_opened
            # ticket.t_subject = ticket.t_subject.capitalize()

            if ticket.t_status.name == "Closed":
                ticket.t_closed = timezone.now()

            ticket.save()
            return redirect("ticketing_index")
    else:
        # print("WE HIT AN ERROR SAVING THE TICKET!!!!!", file=sys.stderr)
        form = EditTicketForm(
            t_status=t_status,
            status_choices=status_choices,
            t_subject=t_subject,
            t_body=t_body,
            t_category=t_category,
            category_choices=category_choices,
        )

    context = {"form": form}

    # return render(request, 'edit_ticket.html', context)
    return render(request, "ticket_detail.html", context)