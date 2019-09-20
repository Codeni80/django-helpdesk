from django.shortcuts import render
from ticketing.models import Technician, Ticket, Customer, Category, Status, TicketTable
from django.views.generic import ListView
from django_tables2 import RequestConfig
import sys

def ticketing_index(request):
    num = request.session.get('sort')
    if not num:
        num = '-pk'
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