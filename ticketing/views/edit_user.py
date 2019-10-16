from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from ticketing.models import CustomUser, UsersTable
from ticketing.forms import (
    EditUserForm,
    EditTicketForm,
    CustomUserCreationForm,
    CustomUserChangeForm,
    UserSearchForm,
    EditUserPasswordForm
)
from django.utils import timezone
from django_tables2 import RequestConfig
from django.db.models.functions import Lower
import sys
from django.contrib.auth.hashers import make_password


@login_required
def user_search(request):
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        if request.user.u_permission_level != "2":
            return redirect("/")
        else:
            if request.method == "POST":
                form = UserSearchForm(request.POST)
                if form.is_valid():
                    result = form.cleaned_data["s_filter"]
                    result = result.lower()
                    val = CustomUser.objects.filter(username__contains=result)
                    if not val:
                        result = result.title()
                        val = CustomUser.objects.filter(u_name__contains=result)
                        if not val:
                            messages.error(request, "User Not Found!")
                            return redirect("/accounts/edit_user")
                        else:
                            table = UsersTable(val)
                            return redirect(
                                "/accounts/search_results/?result={}".format(result)
                            )
                    else:
                        return redirect(
                            "/accounts/search_results/?result={}".format(result)
                        )
            else:
                form = UserSearchForm()
            return render(request, "edit_user.html", {"form": form})


@login_required
def search_results(request):
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        if request.user.u_permission_level != "2":
            return redirect("/")
        else:
            result = request.GET["result"]
            username_val = CustomUser.objects.filter(username__contains=result)
            u_name_val = CustomUser.objects.filter(u_name__contains=result)
            val = username_val | u_name_val
            print(val)
            table = UsersTable(val)
            RequestConfig(request).configure(table)
            return render(request, "user_search_results.html", {"table": table})


@login_required
def reset_password(request, pk=None):
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        current_user = request.user
        if current_user.u_permission_level != "2":
            return redirect("/")
        else:
            user = CustomUser.objects.get(pk=pk)
            updating_pk = user.pk
            updating_username = user.username
            updating_u_name = user.u_name
            updating_pw = user.password
            updating_phone = user.u_phone
            updating_email = user.email
            updating_perms = user.u_permission_level
            perm_choices = (("1", "User"), ("2", "Technician"))

            context = {"user": user}
            if request.method == "POST":
                form = EditUserPasswordForm(
                    request.POST, password=user.password, username=user.username
                )
                if form.is_valid():
                    user = form.save(commit=False)
                    user.pk = updating_pk
                    user.username = updating_username
                    user.u_name = updating_u_name
                    user.u_phone = updating_phone
                    user.email = updating_email
                    user.password = make_password(form.cleaned_data["password"])
                    user.force_change = True
                    user.u_permission_level = updating_perms

                    user.save()
                    return redirect("ticketing_index")
            else:
                # print("WE HIT AN ERROR SAVING THE TICKET!!!!!", file=sys.stderr)
                form = EditUserPasswordForm(password=user.password, username=user.username)

            context = {"form": form}

            # return render(request, 'edit_ticket.html', context)
            return render(request, "edit_user.html", context)

@login_required
def update_user(request, pk=None):
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        current_user = request.user
        if current_user.u_permission_level != "2":
            return redirect("/")
        else:
            user = CustomUser.objects.get(pk=pk)
            updating_pk = user.pk
            updating_username = user.username
            updating_u_name = user.u_name
            updating_phone = user.u_phone
            updating_email = user.email
            updating_perms = user.u_permission_level
            perm_choices = (("1", "User"), ("2", "Technician"))

            context = {"user": user}
            if request.method == "POST":
                form = CustomUserChangeForm(request.POST,
                    u_name=user.u_name,
                    username=user.username,
                    u_phone=user.u_phone,
                    email=user.email,
                    u_permission_level=user.u_permission_level,
                    is_superuser=user.is_superuser,
                    is_staff=user.is_staff,
                    instance=user,
                )
                if form.is_valid():
                    user = form.save()
                    return redirect("ticketing_index")
            else:
                # print("WE HIT AN ERROR SAVING THE TICKET!!!!!", file=sys.stderr)
                form = CustomUserChangeForm(
                    u_name=user.u_name,
                    username=user.username,
                    u_phone=user.u_phone,
                    email=user.email,
                    u_permission_level=user.u_permission_level,
                    is_superuser=user.is_superuser,
                    is_staff=user.is_staff,
                    instance=user,
                )

            context = {"form": form}

            # return render(request, 'edit_ticket.html', context)
            return render(request, "edit_user.html", context)
