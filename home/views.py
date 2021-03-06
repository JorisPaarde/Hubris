from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

from battle.models import Game

# Create your views here.


def main_menu(request):
    """view to return main menu page"""

    return render(request, 'home/index.html')


def how_to_play(request):
    """view to return how to play page"""

    return render(request, 'how-to-play/how-to-play.html')


def leaderboard(request):
    """view to return how to play page"""
    # Get games least gamefloors played, highest score
    games = Game.objects.all().order_by(
        'total_gamefloors_played', '-score')
    # filter the completed games
    games = games.filter(completed=True)
    # filter the games that finished the game
    games = games.filter(current_game_floor_number=15)
    # cap off the list at 10 tp scores
    games = games[:10]
    template = "leaderboard/leaderboard.html"
    context = {
        "games": games,
    }

    return render(request, template, context)

# https://overiq.com/django-1-10/django-creating-users-using-usercreationform/


def register_request(request):
    """view to return register page"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account created successfully')
            return redirect("home:main-menu")

    else:
        form = CustomUserCreationForm()

    template = "register/register.html"

    context = {"form": form}

    return render(request, template, context)

# https://overiq.com/django-1-10/django-creating-users-using-usercreationform/


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
                return redirect("home:main-menu")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()

    template = "login/login.html"

    context = {"login_form": form}

    return render(request, template, context)


@login_required(login_url='home:login')
def logout_request(request):
    """view to log out to main page"""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home:main-menu")


@login_required(login_url='home:login')
def full_version(request):
    """view to return buy full version page"""

    return render(request, 'full-version/full-version.html')
