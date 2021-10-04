from django.shortcuts import render
from .models import Player, Game, Current_game_floor, Enemy, Game_floor_enemy
from profiles.models import Card
from django.contrib import messages

# Create your views here.


def battle_screen(request, game):
    """view to return battle_screen page"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    cards = Card.objects.all()
    game = Game.objects.get(player=player)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    if game.game_step == '1':
        messages.info(request, "Please select a card to play.")

    context = {
        "game": game,
        "current_game_floor": current_game_floor,
        "player": player,
        "cards": cards,
    }

    return render(request, 'battle/battle.html', context)
