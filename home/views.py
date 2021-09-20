from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.


def main_menu(request):
    """view to return main menu page"""

    return render(request, 'home/index.html')


def how_to_play(request):
    """view to return how to play page"""

    return render(request, 'how-to-play/how-to-play.html')

# https://www.ordinarycoders.com/blog/article/django-allauth


def register_request(request):
    """view to return register page"""
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
        else:
            messages.error(request, "Account creation failed {error}")

        return redirect("home:main_menu")

    form = NewUserForm()

    template = "register/register.html"

    context = {"form": form}

    return render(request, template, context)

# https://www.ordinarycoders.com/blog/article/django-allauth


def login_request(request):
    """view to return login page"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home:main_menu")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()

    template = "login/login.html"

    context = {"login_form": form}

    return render(request, template, context)


def logout_request(request):
    """view to log out to main_page"""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home:main_menu")
