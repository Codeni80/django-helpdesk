from django.shortcuts import render
from ticketing.models import Technician, Ticket, Customer, Category, Status, TicketTable
from django.views.generic import ListView
from django_tables2 import RequestConfig

def ticketing_index(request):
    queryset = Ticket.objects.all().order_by('-pk')
    table = TicketTable(queryset)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    return render(request, 'ticketing_index.html', {'table': table})