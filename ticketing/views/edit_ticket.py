from ticketing.models import *
from ticketing.forms import *
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django_tables2 import RequestConfig
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models.functions import Lower
import sys


@login_required
def ticket_detail(request, pk):
    print("PK: {}".format(pk), file=sys.stderr)
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        current_user = request.user
        ticket = Ticket.objects.get(pk=pk)
        updating_pk = ticket.pk
        updating_c_info = ticket.c_info
        updating_t_info = ticket.t_assigned
        updating_timestamp = ticket.timestamp
        updating_opened = ticket.t_opened
        status_query = Status.objects.all()
        t_subject = ticket.t_subject
        t_status = ticket.t_status
        category_query = Category.objects.all()
        t_category = ticket.t_category.pk
        t_category_name = ticket.t_category


        if str(t_category_name) == 'Equipment or Room Setup':
            equipsetup = EquipmentSetup.objects.get(ticket=ticket)
            equip_room = equipsetup.room
            equip_date = equipsetup.date
            equip_start_time = equipsetup.start_time
            equip_end_time = equipsetup.end_time
            equip_t_body = equipsetup.t_body
            equip_pk = equipsetup.pk
            flag = 0
        elif str(t_category_name) == 'Laptop Checkout':
            laptopcheckout = LaptopCheckout.objects.get(ticket=ticket)
            laptop_reason = laptopcheckout.reason
            laptop_start_time = laptopcheckout.start_time
            laptop_end_time = laptopcheckout.end_time
            laptop_l_body = laptopcheckout.l_body
            laptop_pk = laptopcheckout.pk
            flag = 1
        elif str(t_category_name) == 'Printers':
            printers = Printers.objects.get(ticket=ticket)
            printer_problem = printers.problem
            printer_printer = printers.printer
            printer_p_body = printers.p_body
            printer_pk = printers.pk
            flag = 2
        elif str(t_category_name) == 'New Staff':
            newstaff = NewStaff.objects.get(ticket=ticket)
            staff_name = newstaff.name
            staff_department = newstaff.department
            staff_supervisor = newstaff.supervisor
            staff_empid = newstaff.empid
            staff_start_date = newstaff.start_date
            staff_ns_body = newstaff.ns_body
            staff_pk = newstaff.pk
            flag = 3
        elif str(t_category_name) == 'Training':
            training = Training.objects.get(ticket=ticket)
            training_type = training.training_type
            training_staff_name = training.staff_name
            training_location = training.location
            training_date = training.date
            training_tr_body = training.tr_body
            training_pk = training.pk
            flag = 4
        elif str(t_category_name) == 'Password Reset':
            password = PasswordReset.objects.get(ticket=ticket)
            password_name = password.name
            password_account = password.account
            password_pr_body = password.pr_body
            password_pk = password.pk
            flag = 5
        else:
            default = DefaultTicket.objects.get(ticket=ticket)
            default_body = default.ticket_body
            default_pk = default.pk
            flag = 6

        if request.method == "POST":
            form_flag = 0
            c_form = CommentForm(request.POST)
            c_form.author = current_user
            form = EditTicketForm(
                request.POST,
                t_status = t_status,
                t_subject = t_subject,
                t_category = t_category,
                updating_t_info = updating_t_info,
                perm_level = request.user.u_permission_level
            )
            status = Status.objects.get(name=form.t_status)
            ticket.status = status
            if flag == 0:
                sec_form = EditEquipRoomForm(
                    request.POST,
                    room = equip_room,
                    date = equip_date,
                    start_time = equip_start_time,
                    end_time = equip_end_time,
                    t_body = equip_t_body
                )
            elif flag == 1:
                sec_form = EditLaptopCheckoutForm(
                    request.POST,
                    reason = laptop_reason,
                    start_time = laptop_start_time,
                    end_time = laptop_end_time,
                    l_body = laptop_l_body
                )
            elif flag == 2:
                sec_form = EditPrintersForm(
                    request.POST,
                    problem = printer_problem,
                    printer = printer_printer,
                    p_body = printer_p_body
                )
            elif flag == 3:
                sec_form = EditNewStaffForm(
                    request.POST,
                    name = staff_name,
                    department = staff_department,
                    supervisor = staff_supervisor,
                    empid = staff_empid,
                    start_date = staff_start_date,
                    ns_body = staff_ns_body
                )
            elif flag == 4:
                sec_form = EditTrainingForm(
                    request.POST,
                    training_type = training_type,
                    staff_name = training_staff_name,
                    location = training_location,
                    date = training_date,
                    tr_body = training_tr_body
                )
            elif flag == 5:
                sec_form = EditPasswordResetForm(
                    request.POST,
                    name = password_name,
                    account = password_account,
                    pr_body = password_pr_body
                )
            elif flag == 6:
                print("FLAG SIX", file=sys.stderr)
                sec_form = EditDefaultTicketForm(
                    request.POST,
                    ticket_body = default_body
                )

            if c_form.is_valid():
                print("COMMENT FORM VALID", file=sys.stderr)
                comment = Comment(
                    author = current_user,
                    body = c_form.cleaned_data["body"],
                    ticket = ticket,
                    is_private = c_form.cleaned_data["is_private"]
                )
                comment.save()
                return HttpResponseRedirect('/ticket_detail/{}'.format(ticket.pk))
            

            if form.is_valid():
                print("Base form is valid.", file=sys.stderr)
                ticket = form.save(commit=False)
                ticket.pk = updating_pk
                ticket.status = status
                ticket.c_info = updating_c_info
                ticket.assigned = updating_t_info
                ticket.timestamp = updating_timestamp
                ticket.t_opened = updating_opened

                if ticket.t_status.name == "Closed":
                    ticket.t_closed = timezone.now()
                    ticket.days_opened = ticket.t_closed - ticket.t_opened
                    ticket.days_opened = str(ticket.days_opened).split('.', 1)
                    ticket.days_opened = ticket.days_opened[0]
                
                
                ticket.save()
                if flag == 0:
                    if sec_form.is_valid():
                        equipmentroom = sec_form.save(commit=False)
                        equipmentroom.pk = equip_pk
                        equipmentroom.room = sec_form.cleaned_data['room']
                        equipmentroom.date = sec_form.cleaned_data['date']
                        equipmentroom.start_time = sec_form.cleaned_data['start_time']
                        equipmentroom.end_time = sec_form.cleaned_data['end_time']
                        equipmentroom.t_body = sec_form.cleaned_data['t_body']
                        equipmentroom.ticket = ticket
                        equipmentroom.save()
                    else:
                        form_flag = 1
                elif flag == 1:
                    if sec_form.is_valid():
                        laptop = sec_form.save(commit=False)
                        laptop.pk = laptop_pk
                        laptop.reason = sec_form.cleaned_data['reason']
                        laptop.start_time = sec_form.cleaned_data['start_time']
                        laptop.end_time = sec_form.cleaned_data['end_time']
                        laptop.l_body = sec_form.cleaned_data['l_body']
                        laptop.ticket = ticket
                        laptop.save()
                    else:
                        form_flag = 1
                elif flag == 2:
                    if sec_form.is_valid():
                        printer = sec_form.save(commit=False)
                        printer.problem = sec_form.cleaned_data['problem']
                        printer.printer = sec_form.cleaned_data['printer']
                        printer.p_body = sec_form.cleaned_data['p_body']
                        printer.pk = printer_pk
                        printer.ticket = ticket
                        printer.save()
                    else:
                        form_flag = 1
                elif flag == 3:
                    if sec_form.is_valid():
                        staff = sec_form.save(commit=False)
                        staff.name = sec_form.cleaned_data['name']
                        staff.department = sec_form.cleaned_data['department']
                        staff.supervisor = sec_form.cleaned_data['supervisor']
                        staff.empid = sec_form.cleaned_data['empid']
                        staff.start_date = sec_form.cleaned_data['start_date']
                        staff.pk = staff_pk
                        staff.ns_body = sec_form.cleaned_data['ns_body']
                        staff.ticket = ticket
                        staff.save()
                    else:
                        form_flag = 1
                elif flag == 4:
                    if sec_form.is_valid():
                        straining = sec_form.save(commit=False)
                        straining.type = sec_form.cleaned_data['training_type']
                        straining.staff_name = sec_form.cleaned_data['staff_name']
                        straining.location = sec_form.cleaned_data['location']
                        straining.date = sec_form.cleaned_data['date']
                        straining.pk = training_pk
                        straining.ticket = ticket
                        straining.save()
                    else:
                        form_flag = 1
                elif flag == 5:
                    if sec_form.is_valid():
                        passreset = sec_form.save(commit=False)
                        passreset.name = sec_form.cleaned_data['name']
                        passreset.account = sec_form.cleaned_data['account']
                        passreset.pr_body = sec_form.cleaned_data['pr_body']
                        passreset.pk = password_pk
                        passreset.ticket = ticket
                        passreset.save()
                    else:
                        form_flag = 1
                elif flag == 6:
                    print("We hit flag 6 (Default ticket)", file=sys.stderr)
                    if sec_form.is_valid():
                        defticket = sec_form.save(commit=False)
                        defticket.ticket_body = sec_form.cleaned_data['ticket_body']
                        defticket.pk = default_pk
                        defticket.ticket = ticket
                        defticket.save()
                    else:
                        form_flag = 1
                if form_flag == 0:
                    print("Form worked", file=sys.stderr)
                    messages.success(
                        request,
                        "<strong>Success!</strong> Ticket <a class='text-dark' href='ticket_detail/{0}'><strong><u>#{0}</u></strong></a> Has Been Updated!".format(
                            ticket.pk
                        ),
                        extra_tags="safe",
                    )
                    return redirect("ticketing_index")
                else:
                    print("Error with form", file=sys.stderr)
                    messages.error(request, "Error: Form is invalid, please check information entered and try again.")
                    return redirect(request.META['HTTP_REFERER'])
        else:
            if flag == 0:
                sec_form = EditEquipRoomForm(
                    room = equip_room,
                    date = equip_date,
                    start_time = equip_start_time,
                    end_time = equip_end_time,
                    t_body = equip_t_body
                )
            elif flag == 1:
                sec_form = EditLaptopCheckoutForm(
                    reason = laptop_reason,
                    start_time = laptop_start_time,
                    end_time = laptop_end_time,
                    l_body = laptop_l_body
                )
            elif flag == 2:
                sec_form = EditPrintersForm(
                    problem = printer_problem,
                    printer = printer_printer,
                    p_body = printer_p_body
                )
            elif flag == 3:
                sec_form = EditNewStaffForm(
                    name = staff_name,
                    department = staff_department,
                    supervisor = staff_supervisor,
                    empid = staff_empid,
                    start_date = staff_start_date,
                    ns_body = staff_ns_body
                )
            elif flag == 4:
                sec_form = EditTrainingForm(
                    training_type = training_type,
                    staff_name = training_staff_name,
                    location = training_location,
                    date = training_date,
                    tr_body = training_tr_body
                )
            elif flag == 5:
                sec_form = EditPasswordResetForm(
                    name = password_name,
                    account = password_account,
                    pr_body = password_pr_body 
                )
            elif flag == 6:
                sec_form = EditDefaultTicketForm(
                    ticket_body = default_body
                )
            print(request.user.u_permission_level, file=sys.stderr)
            form = EditTicketForm(
                t_status = t_status,
                t_subject = t_subject,
                t_category = t_category,
                updating_t_info = updating_t_info,
                perm_level = request.user.u_permission_level
            )
            c_form = CommentForm()
        if current_user.u_permission_level == '2':
            comments = Comment.objects.filter(ticket=ticket)
        else:
            comments = Comment.objects.filter(ticket=ticket, is_private=False)

        context = {
            "form": form,
            "sec_form": sec_form,
            "c_form": c_form,
            "comments": comments
        }

        return render(request, "ticket_detail.html", context)
