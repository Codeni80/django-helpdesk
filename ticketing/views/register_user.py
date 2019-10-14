from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from ticketing.models import CustomUser
from ticketing.forms import CustomUserCreationForm
from django.utils import timezone
import sys

@login_required
def register(request):
<<<<<<< HEAD
    if request.user.force_change == True:
        return redirect("change_password")
    else:
        if request.user.u_permission_level != "2":
            return redirect("/")
        else:
            if request.method == "POST":
                form = CustomUserCreationForm(request.POST)
                if form.is_valid():
                    new_user = form.save(commit=False)
                    u_name = form.cleaned_data["u_name"]
                    username = form.cleaned_data["username"]
                    email = form.cleaned_data["email"]
                    # print("FORM VARIABLE FROM FORM: {0}".format(form), file=sys.stderr)
                    new_user.u_name = u_name.title()
                    new_user.username = username.lower()
                    new_user.email = email.lower()
                    form.save()
                    username = form.cleaned_data.get("username")
                    raw_password = form.cleaned_data.get("password1")
                    user = authenticate(username=username, password=raw_password)
                    # login(request, user)
                    return redirect("/")
            else:
                form = CustomUserCreationForm()
            return render(request, "register.html", {"form": form})
=======
    current_user = request.user
    if current_user.u_permission_level == "2":
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                u_name = form.cleaned_data["u_name"]
                username = form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                # print("FORM VARIABLE FROM FORM: {0}".format(form), file=sys.stderr)
                new_user.u_name = u_name.title()
                new_user.username = username.lower()
                new_user.email = email.lower()
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                # login(request, user)
                return redirect("/")
        else:
            form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})
    else:
        return redirect('ticketing_index')
>>>>>>> 4e14eb17b6c48cb377b66478e3db61433db7f7b1
