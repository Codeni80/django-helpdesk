from django.shortcuts import render, redirect
from ticketing.models import Ticket, Category, Status, TicketTable
from django.views.generic import ListView
from django_tables2 import RequestConfig
import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .forms import CustomUserCreationForm, TicketForm
from django.forms import ModelForm
from django.utils import timezone

@login_required
def ticketing_index(request):
    num = request.session.get('sort')
    if not num:
        num = '-pk'
        request.session['sort'] = num
    try:
        request.session['sort'] = request.GET['sort']
        num = request.session['sort']
    except:
        pass

    print(request.session.get('sort'), file=sys.stderr)
    sort_by = request.session.get('sort')

    queryset = Ticket.objects.all().order_by(sort_by)
    table = TicketTable(queryset)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    return render(request, 'ticketing_index.html', {'table': table})

def ticket_detail(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    context = {
        "ticket": ticket
    }
    return render(request, "ticket_detail.html", context)

def register(request):
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def new_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.c_info = request.user
            ticket.timestamp = timezone.now()
            ticket.t_opened = timezone.now()
            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    
    context = {
        'form': form,
    }

    return render(request, 'new_ticket.html', context)
    # form = TicketForm()
    # return render(request, '/', {'form': form})
