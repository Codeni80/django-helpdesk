from django.shortcuts import render, redirect
from ticketing.models import Ticket, Category, Status, TicketTable
from django.views.generic import ListView
from django_tables2 import RequestConfig
import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from ticketing.models import CustomUser
from ticketing.forms import CustomUserCreationForm, TicketForm, EditTicketForm
from django.forms import ModelForm
from django.utils import timezone
from django.db.models.functions import Lower
from django.contrib import messages


@login_required
def new_ticket(request):
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        t_choices = [(0, "---------")]
        techs = get_user_model()
        techs = techs.objects.filter(u_permission_level=2)
        user_obj = request.user
        perm_level = user_obj.u_permission_level
        user = user_obj.u_name
        c_choices = CustomUser.objects.all()

        if request.method == "POST":
            form = TicketForm(
                request.POST,
                t_choices=techs,
                perm_level=perm_level,
                u_name=user_obj,
                c_choices=c_choices,
            )
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.timestamp = timezone.now()
                ticket.t_opened = timezone.now()
                ticket.t_subject = ticket.t_subject.capitalize()

                if ticket.t_status.name == "Closed":
                    # We set the current time to ticket.t_closed
                    # Only if t_status is set to closed
                    ticket.t_closed = timezone.now()

                ticket.save()
                queryset = Ticket.objects.all()

                # return redirect("ticket_detail", pk=ticket.pk)
                messages.success(
                    request,
                    "<strong>Success!</strong> Created Ticket <a class='text-dark' href='ticket_detail/{0}'><strong><u>#{0}</u></strong></a>!".format(
                        ticket.pk
                    ),
                    extra_tags="safe",
                )
                return redirect("ticketing_index")
        else:
            form = TicketForm(
                t_choices=techs,
                perm_level=perm_level,
                u_name=user_obj,
                c_choices=c_choices,
            )

        context = {"form": form}

        return render(request, "new_ticket.html", context)
