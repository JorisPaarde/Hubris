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
        # connect this player to the current user
        current_user = request.user
        selected_type = Player_type.objects.get(selected=selected)

        if str(selected_type):
            # values set for fire wizard
            if str(selected_type) == 'FR':
                player = Player(type=selected_type,
                                user=current_user,
                                fire_attack_power=3,
                                fire_defense=3,
                                mana_max=4,
                                health_max=10
                                )
                player.save()
            # values set for lightning wizard
            elif str(selected_type) == 'LN':
                player = Player(type=selected_type,
                                user=current_user,
                                lightning_attack_power=3,
                                lightning_defense=3,
                                mana_max=4,
                                health_max=10
                                )
                player.save()
            # values set for ice wizard
            elif str(selected_type) == 'IC':
                player = Player(type=selected_type,
                                user=current_user,
                                ice_attack_power=3,
                                ice_defense=3,
                                mana_max=4,
                                health_max=2
                                )
                player.save()

        # get a list of cards available to this player
        # available_cards = Card.objects.filter(in_freeversion=True)
        # add 8 cards to hand
        # for card in range(8) add to hand

    return render(request, 'battle/battle.html')
