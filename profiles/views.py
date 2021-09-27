from django.shortcuts import render
from .models import Player_type, Player, Card

# Create your views here.


def player_select(request):
    """view to return player selection page"""

    player_type = Player_type.objects.all()

    context = {
        'player_type': player_type,
    }

    return render(request, 'profiles/player-select.html', context)


def game_setup(request, selected):

    if request.method == 'POST':
        # create a new player and set the initial values for that player
        # set player type
        selected_type = Player_type.objects.get(selected=selected)
        player = Player(type=selected_type)
        player.save()
        # connect this player to the current user
        
        # get a list of cards available to this player
        # available_cards = Card.objects.filter(in_freeversion=True)
        # add 8 cards to hand
        # for card in range(8) add to hand

    return render(request, 'battle/battle.html')
