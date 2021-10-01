from django.shortcuts import render
from .models import Player, Game, Current_game_floor, Enemy, Game_floor_enemy
from profiles.models import Card

# Create your views here.


def battle_screen(request):
    """view to return battle_screen page"""
    current_user = request.user
    player = Player.objects.get(user=current_user)
    cards = Card.objects.all()

    foo = "Foo"
    bar = "Foo"

    context = {
        'player': player,
        'cards': cards,
        'foo': foo,
        'bar': bar,
    }

    return render(request, 'battle/battle.html', context)
