from ticketing.models import Ticket, Comment, Category, Status, TicketTable, CustomUser
from ticketing.forms import CustomUserCreationForm, CommentForm, TicketForm, EditTicketForm
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
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        current_user = request.user
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

        context = {"ticket": ticket}
        if request.method == "POST":
            c_form = CommentForm(request.POST)
            c_form.author = current_user
            form = EditTicketForm(
                request.POST,
                t_status=t_status,
                status_choices=status_choices,
                t_subject=t_subject,
                t_body=t_body,
                t_category=t_category,
                category_choices=category_choices,
            )
            status = Status.objects.filter(name=form.t_status)
            ticket.status = status
            print("Ticket.status: {0}".format(ticket.status), file=sys.stderr)
            print("C_FORM: {}".format(c_form.is_valid()), file=sys.stderr)
            if c_form.is_valid():
                comment = Comment(
                    author = current_user,
                    body = c_form.cleaned_data["body"],
                    ticket = ticket,
                    is_private = c_form.cleaned_data["is_private"]
                )
                print("TICKET: {}".format(ticket), file=sys.stderr)
                comment.save()
                return HttpResponseRedirect('/ticket_detail/{}'.format(ticket.pk))
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.pk = updating_pk
                ticket.status = status
                ticket.c_info = updating_cinfo
                ticket.t_assigned = updating_tinfo
                ticket.timestamp = updating_ts
                ticket.t_opened = updating_opened
                # ticket.t_subject = ticket.t_subject.capitalize()

                if ticket.t_status.name == "Closed":
                    ticket.t_closed = timezone.now()
                    ticket.days_opened = ticket.t_closed - ticket.t_opened
                    ticket.days_opened = str(ticket.days_opened).split('.', 1)
                    ticket.days_opened = ticket.days_opened[0]

                ticket.save()
                messages.success(
                    request,
                    "<strong>Success!</strong> Ticket <a class='text-dark' href='ticket_detail/{0}'><strong><u>#{0}</u></strong></a> Has Been Updated!".format(
                        ticket.pk
                    ),
                    extra_tags="safe",
                )
                return redirect("ticketing_index")
        else:
            # print("WE HIT AN ERROR SAVING THE TICKET!!!!!", file=sys.stderr)
            form = EditTicketForm(
                t_status=t_status,
                status_choices=status_choices,
                t_subject=t_subject,
                t_body=t_body,
                t_category=t_category,
                category_choices=category_choices,
            )
            c_form = CommentForm()
        if current_user.u_permission_level == "2":
            comments = Comment.objects.filter(ticket=ticket)
        else:
            comments = Comment.objects.filter(ticket=ticket, is_private=False)
        context = {
            "form": form,
            "c_form": c_form,
            "comments": comments
        }

        # return render(request, 'edit_ticket.html', context)
        return render(request, "ticket_detail.html", context)
