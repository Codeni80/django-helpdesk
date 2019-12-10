from django.shortcuts import render, redirect
from ticketing.models import Ticket, Category, Status, TicketTable
from django.views.generic import ListView
from django_tables2 import RequestConfig
import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from ticketing.models import CustomUser, EquipmentSetup
from ticketing.forms import EquipRoomForm, TicketTypeForm, CustomUserCreationForm, TicketForm, EditTicketForm
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
        t_type = request.GET['type']
        print(t_type, file=sys.stderr)
        if request.method == "POST":
            if t_type == 'Dynamics' or t_type == 'Email' or t_type == 'General Computer Issue' or t_type == 'Microsoft Office' or t_type == 'Majestic' or t_type == 'Other' or t_type == 'Smart Card':
                t_type = Category.objects.filter(name=t_type)
                for t in t_type:
                    result = t
                t_type = result
                form = TicketForm(
                    request.POST,
                    t_choices=techs,
                    perm_level=perm_level,
                    u_name=user_obj,
                    c_choices=c_choices,
                )
            elif t_type == 'Equipment or Room Setup':
                t_type = Category.objects.filter(name=t_type)
                for t in t_type:
                    result = t
                t_type = result
                form = TicketForm(
                    request.POST,
                    t_choices=techs,
                    perm_level=perm_level,
                    u_name=user_obj,
                    c_choices=c_choices,
                )
                sec_form = EquipRoomForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.t_category = t_type
                ticket.timestamp = timezone.now()
                ticket.t_opened = timezone.now()
                ticket.t_subject = ticket.t_subject.capitalize()

                if ticket.t_status.name == "Closed":
                    # We set the current time to ticket.t_closed
                    # Only if t_status is set to closed
                    ticket.t_closed = timezone.now()
                    ticket.days_opened = ticket.t_closed - ticket.t_opened
                    ticket.days_opened = str(ticket.days_opened).split('.', 1)
                    ticket.days_opened = ticket.days_opened[0]
                    print(ticket.days_opened, file=sys.stderr)
                
                ticket.save()
                ticket = Ticket.objects.get(pk=ticket.pk)
                print("TICKET: {}".format(ticket.pk), file=sys.stderr)
                
            if sec_form.is_valid():
                equipmentsetup = EquipmentSetup(
                    room = sec_form.cleaned_data['room'],
                    date = sec_form.cleaned_data['date'],
                    start_time = sec_form.cleaned_data['start_time'],
                    end_time = sec_form.cleaned_data['end_time'],
                    ticket = ticket
                )
                equipmentsetup.save()

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
                messages.error(request, 'Error: {}'.format(sec_form.is_valid()))
        else:
            if t_type == 'Dynamics' or t_type == 'Email' or t_type == 'General Computer Issue' or t_type == 'Microsoft Office' or t_type == 'Majestic' or t_type == 'Other' or t_type == 'Smart Card':
                form = TicketForm(
                    t_choices=techs,
                    perm_level=perm_level,
                    u_name=user_obj,
                    c_choices=c_choices,
                )
            elif t_type == 'Equipment or Room Setup':
                form = TicketForm(
                    t_choices=techs,
                    perm_level=perm_level,
                    u_name=user_obj,
                    c_choices=c_choices,
                )
                sec_form = EquipRoomForm()
        if t_type == 'Equipment or Room Setup':
            context = {'form': form, 'sec_form': sec_form}
        else:
            context = {"form": form}

        return render(request, "new_ticket.html", context)


def ticket_type(request):
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        if request.method == "POST":
            form = TicketTypeForm(request.POST)
            if form.is_valid():
                t_type = form.cleaned_data['t_type']
                context = {'t_type': t_type}
                return redirect("/new_ticket/?type={}".format(t_type))
        else:
            form = TicketTypeForm()
        context = {"form": form}
        return render(request, "ticket_type.html", context)
