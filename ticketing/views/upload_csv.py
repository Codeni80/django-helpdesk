from django.shortcuts import render, redirect, HttpResponsePermanentRedirect
from ticketing.models import Ticket, Category, Status, CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.utils import timezone
from django.db.models.functions import Lower
from django.urls import reverse
from ticketing.forms import TicketForm
import sys

@login_required
def upload_csv(request):
    data = {}
    current_user = request.user
    if current_user.u_permission_level == "2":
        if "GET" == request.method:
            return render(request, 'upload_csv.html', data)
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "File is not the correct type")
                return HttpResponsePermanentRedirect(reverse('upload_csv'))
            if csv_file.multiple_chunks():
                print("FILE SIZE IS TOO LARGE")
                return HttpResponsePermanentRedirect(reverse('upload_csv'))
            file_data = csv_file.read().decode('utf-8')

            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['t_opened'] = fields[0]
                data_dict['c_name'] = fields[1]
                data_dict['t_subject'] = fields[2]
                data_dict['t_status'] = fields[3]
                data_dict['t_assigned'] = fields[4]
                data_dict['t_closed'] = fields[6]
                try:
                    user = get_user_model()
                    user = user.objects.filter(u_permission_level=2)
                    form = TicketForm(data_dict, t_choices=user)
                    print("FORM: {0} | DATA_DICT: {1}".format(form, data_dict))
                    if form.is_valid():
                        print("We saved the ticket?")
                        form.save()
                    else:
                        print('error saving csv')
                except Exception as e:
                    print("ERROR: {}".format(e))
                    pass
        except Exception as e:
            print("OUTER ERROR: {}".format(e))
        
        return HttpResponsePermanentRedirect(reverse('upload_csv'))
    else:
        return redirect('ticketing_index')
