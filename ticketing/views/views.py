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

@login_required
def ticketing_index(request):
    current_user = request.user
    user = get_user_model()

    # Checking for sort type, setting it if we can
    if not current_user.u_sort_type:
        current_user.u_sort_type = '-pk' #Setting default sort to sort newest to oldest tickets
    try:
        #Try to set the sort type to what is requested by user
        current_user.u_sort_type = request.GET['sort']
        current_user.save()
        print("WE SAVED THE SORT TYPE", file=sys.stderr)
    except:
        print('WE HAD AN ERROR SAVING THE SORT TYPE', file=sys.stderr)

    sort_by = current_user.u_sort_type
    print("Sorting by: {0}".format(sort_by), file=sys.stderr)

    if(current_user.u_permission_level == '2'):
        queryset = Ticket.objects.all().order_by(sort_by)
        table = TicketTable(queryset)
        RequestConfig(request, paginate={"per_page": 20}).configure(table)

        return render(request, 'ticketing_index.html', {'table': table})
    else:
        queryset = Ticket.objects.filter(c_info__username=current_user.username).order_by(sort_by)
        # print("Queryset: {0}".format(queryset), file=sys.stderr)
        # test = user.objects.filter(username=current_user.username)
        # print("Current User: {0}".format(test), file=sys.stderr)
        table = TicketTable(queryset)
        RequestConfig(request, paginate={"per_page": 20}).configure(table)

        return render(request, 'ticketing_index.html', {'table': table})


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

    context = {
        "ticket": ticket
    }
    if request.method == "POST":
        form = EditTicketForm(request.POST, t_status=t_status, status_choices=status_choices, t_subject=t_subject, t_body=t_body, t_category=t_category, category_choices=category_choices)
        status = Status.objects.filter(name=form.t_status)
        # print("Status from Form: {0}".format(form.t_status), file=sys.stderr)
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

            if ticket.t_status.name == 'Closed':
                ticket.t_closed = timezone.now()

            ticket.save()
            return redirect('ticketing_index')
    else:
        # print("WE HIT AN ERROR SAVING THE TICKET!!!!!", file=sys.stderr)
        form = EditTicketForm(t_status= t_status, status_choices=status_choices, t_subject=t_subject, t_body=t_body, t_category=t_category, category_choices=category_choices)
    
    context = {
        'form': form,
    }

    # return render(request, 'edit_ticket.html', context)
    return render(request, "ticket_detail.html", context)

@login_required
def new_ticket(request):
    t_choices = [(0, '---------')]
    user = get_user_model()
    user = user.objects.filter(u_permission_level=2)
    
    if request.method == "POST":
        form = TicketForm(request.POST, t_choices=user)
        if form.is_valid():
            ticket = form.save(commit=False)
            # ticket.c_info = request.user
            ticket.timestamp = timezone.now()
            ticket.t_opened = timezone.now()

            if ticket.t_status.name == 'Closed':
                #We set the current time to ticket.t_closed
                ticket.t_closed = timezone.now()
            
            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(t_choices=user)
    
    context = {
        'form': form,
    }

    return render(request, 'new_ticket.html', context)
    # form = TicketForm()
    # return render(request, '/', {'form': form})
