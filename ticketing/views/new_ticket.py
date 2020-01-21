from django.shortcuts import render, redirect
from ticketing.models import *
from django.views.generic import ListView
from django_tables2 import RequestConfig
import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from ticketing.models import CustomUser, EquipmentSetup
from ticketing.forms import *
from django.forms import ModelForm
from django.utils import timezone
from django.db.models.functions import Lower
from django.contrib import messages


@login_required
def new_ticket(request):
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        t_type = request.GET['type']
        user_obj = request.user
        perm_level = user_obj.u_permission_level
        ticket_type = Category.objects.get(name=t_type)
        tech_group = get_user_model()
        tech_group = tech_group.objects.filter(u_permission_level = 2)
        
        if request.method == 'POST':
            flag = 1
            form = TicketForm(request.POST,
                perm_level = perm_level,
                u_name = user_obj,
                t_choices = tech_group
            )
            if form.is_valid():
                flag = 0

            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.t_subject = ticket.t_subject.capitalize()
                ticket.t_category = ticket_type
                ticket.timestamp = timezone.now()
                ticket.t_opened = timezone.now()

                if ticket.t_status.name == 'Closed':
                    ticket.t_closed = timezone.now()
                    ticket.days_opened = ticket.t_closed - ticket.t_opened
                    ticket.days_opened = str(ticket.days_opened).split('.', 1)
                    ticket.days_opened = ticket.days_opened[0]

                ticket.save()
                ticket = Ticket.objects.get(pk=ticket.pk)

                if t_type == 'Equipment or Room Setup':
                    t_type = Category.objects.get(name=t_type)
                    sec_form = EquipRoomForm(request.POST)
                    if sec_form.is_valid():
                        equipmentsetup = EquipmentSetup(
                            room = sec_form.cleaned_data['room'],
                            date = sec_form.cleaned_data['date'],
                            start_time = sec_form.cleaned_data['start_time'],
                            end_time = sec_form.cleaned_data['end_time'],
                            ticket = ticket
                        )
                        equipmentsetup.save()
                    else:
                        flag = 1
                elif t_type == 'Laptop Checkout':
                    t_type = Category.objects.get(name=t_type)
                    sec_form = LaptopCheckoutForm(request.POST)
                    if sec_form.is_valid():
                        laptopcheckout = LaptopCheckout(
                            reason = sec_form.cleaned_data['reason'],
                            start_time = sec_form.cleaned_data['start_time'],
                            end_time = sec_form.cleaned_data['end_time'],
                            ticket = ticket
                        )
                        laptopcheckout.save()
                    else:
                        flag = 1
                elif t_type == 'Printers':
                    t_type = Category.objects.get(name=t_type)
                    sec_form = PrintersForm(request.POST)
                    if sec_form.is_valid():
                        printers = Printers(
                            problem = sec_form.cleaned_data['problem'],
                            printer = sec_form.cleaned_data['printer'],
                            ticket = ticket
                        )
                        printers.save()
                    else:
                        flag = 1
                elif t_type == 'New Staff':
                    t_type = Category.objects.get(name=t_type)
                    sec_form = NewStaffForm(request.POST)
                    if sec_form.is_valid():
                        newstaff = NewStaff(
                            name = sec_form.cleaned_data['name'],
                            department = sec_form.cleaned_data['department'],
                            supervisor = sec_form.cleaned_data['supervisor'],
                            empid = sec_form.cleaned_data['empid'],
                            start_date = sec_form.cleaned_data['start_date'],
                            ticket = ticket
                        )
                        newstaff.save()
                    else:
                        flag = 1
                elif t_type == 'Training':
                    t_type = Category.objects.get(name=t_type)
                    sec_form = TrainingForm(request.POST)
                    if sec_form.is_valid():
                        training = Training(
                            training_type = sec_form.cleaned_data['training_type'],
                            staff_name = sec_form.cleaned_data['staff_name'],
                            location = sec_form.cleaned_data['location'],
                            date = sec_form.cleaned_data['date'],
                            ticket = ticket
                        )
                        training.save()
                    else:
                        flag = 1
                elif t_type == 'Password Reset':
                    t_type = Category.objects.get(name=t_type)
                    sec_form = PasswordResetForm(request.POST)
                    if sec_form.is_valid():
                        passwordreset = PasswordReset(
                            name = sec_form.cleaned_data['name'],
                            account = sec_form.cleaned_data['account'],
                            ticket = ticket
                        )
                        passwordreset.save()
                    else:
                        flag = 1
                else:
                    t_type = Category.objects.get(name=t_type)
                    sec_form = DefaultTicketForm(request.POST)
                    if sec_form.is_valid():
                        defaultticket = DefaultTicket(
                            body = sec_form.cleaned_data['body'],
                            ticket = ticket
                        )
                        defaultticket.save()
                    else:
                        flag = 1
                if flag == 0:
                    return redirect("ticketing_index")
                else:
                    ticket.delete()
                    messages.error(request, "Error: Form is invalid, please check information entered and try again.")
                    return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, "Error: Form is invalid, please check information entered and try again.")
        else:
            form = TicketForm(
                perm_level = perm_level,
                u_name = user_obj,
                t_choices = tech_group
            )
            if t_type == 'Equipment or Room Setup':
                sec_form = EquipRoomForm()
                context = {'form': form, 'sec_form': sec_form}
            elif t_type == 'Laptop Checkout':
                sec_form = LaptopCheckoutForm()
                context = {'form': form, 'sec_form': sec_form}
            elif t_type == 'Printers':
                sec_form = PrintersForm()
                context = {'form': form, 'sec_form': sec_form}
            elif t_type == 'New Staff':
                sec_form = NewStaffForm()
                context = {'form': form, 'sec_form': sec_form}
            elif t_type == 'Training':
                sec_form = TrainingForm()
                context = {'form': form, 'sec_form': sec_form}
            elif t_type == 'Password Reset':
                sec_form = PasswordResetForm()
                context = {'form': form, 'sec_form': sec_form}
            else:
                sec_form = DefaultTicketForm()
                context = {'form': form, 'sec_form': sec_form}
            return render(request, 'new_ticket.html', context)

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
