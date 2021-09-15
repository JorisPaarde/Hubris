from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# Create your views here.


def main_menu(request):
    """view to return main menu page"""

    return render(request, 'home/index.html')

# https://www.ordinarycoders.com/blog/article/django-allauth


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
        else:
            messages.error(request, "Account creation failed")

        return redirect("home:main_menu")

    form = NewUserForm()

    template = "register/register.html"

    context = {"form": form}

    return render(request, template, context)

# https://www.ordinarycoders.com/blog/article/django-allauth
