from django.shortcuts import render
from ticketing.models import Technician, Ticket, Customer, Category, Status

def ticketing_index(request):
    tickets = Ticket.objects.all().order_by('-t_opened')
    context = {
        'tickets': tickets
    }
    return render(request, 'ticketing_index.html', context)
