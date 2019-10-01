from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from ticketing.models import CustomUser
from ticketing.forms import CustomUserCreationForm
from django.utils import timezone
import sys

def register(request):
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            u_name = form.cleaned_data['u_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            # print("FORM VARIABLE FROM FORM: {0}".format(form), file=sys.stderr)
            new_user.u_name = u_name.title()
            new_user.username = username.lower()
            new_user.email = email.lower()
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
