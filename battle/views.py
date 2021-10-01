from django.shortcuts import render
from .models import Player, Game, Current_game_floor, Enemy, Game_floor_enemy
from profiles.models import Card
from django.contrib import messages

# Create your views here.


def battle_screen(request):
    """view to return battle_screen page"""
    current_user = request.user
    player = Player.objects.get(user=current_user)
    cards = Card.objects.all()
    messages.info(request, "Please select a card to play.")

    context = {
        "player": player,
        "cards": cards,
    }

    return render(request, 'battle/battle.html', context)
