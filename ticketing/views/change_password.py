from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from ticketing.models import CustomUser, UsersTable
from ticketing.forms import (
    PasswordChange,
    EditUserForm,
    EditTicketForm,
    CustomUserCreationForm,
    CustomUserChangeForm,
    UserSearchForm,
)
from django.utils import timezone
from django_tables2 import RequestConfig
from django.db.models.functions import Lower
import sys
from django.contrib.auth.hashers import make_password, check_password


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChange(request.POST)
        if form.is_valid():
            old = check_password(
                form.cleaned_data["old_password"], request.user.password
            )
            print(old)
            if old is True:
                if (
                    form.cleaned_data["new_password"]
                    == form.cleaned_data["confirm_password"]
                ):
                    password = make_password(form.cleaned_data["new_password"])
                    request.user.password = password
                    request.user.force_change = False
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    return redirect("/")
                else:
                    messages.error(request, "Passwords Do Not Match!")
            else:
                messages.error(
                    request, "Old Password was not correct, please try again."
                )

        return render(request, "change_password.html", {"form": form})
    else:
        form = PasswordChange()
        return render(request, "change_password.html", {"form": form})
