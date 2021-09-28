from django.shortcuts import render
from .models import Player_type, Player, Card, Hand_card
from django.conf import settings
import random
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

        # check if this user already has a player (with an unfinished game)
        current_user = request.user
        current_player = Player.objects.filter(user=current_user)

        if not current_player:
            # create a new player and set the initial values for that player
            # get the selected player type
            selected_type = Player_type.objects.get(selected=selected)
            # connect this player to the current user
            player = Player(user=current_user, type=selected_type)
            player.save()

            current_player = player
            # create an empty hand for this player
            hand = Player.hand
            # add 8 cards this hand
            draw_n_cards = 8
            draw_cards(draw_n_cards, hand, current_player)

            if str(selected_type):
                # values set for fire wizard
                if str(selected_type) == 'FR':
                    player = Player(pk=current_player.id,
                                    type=selected_type,
                                    user=current_user,
                                    fire_attack_power=3,
                                    fire_defense=3,
                                    mana_max=4,
                                    health_max=10
                                    )
                    player.save()
                # values set for lightning wizard
                elif str(selected_type) == 'LN':
                    player = Player(pk=current_player.id,
                                    type=selected_type,
                                    user=current_user,
                                    lightning_attack_power=3,
                                    lightning_defense=3,
                                    mana_max=4,
                                    health_max=10
                                    )
                    player.save()
                # values set for ice wizard
                elif str(selected_type) == 'IC':
                    player = Player(pk=current_player.id,
                                    type=selected_type,
                                    user=current_user,
                                    ice_attack_power=3,
                                    ice_defense=3,
                                    mana_max=4,
                                    health_max=2
                                    )
                    player.save()
        else:
            print(current_player)
            print('startgame')
            # start this users game with this player

    return render(request, 'battle/battle.html')


# function to draw new cards for a hand
def draw_cards(n, hand, current_player):

    print(current_player)

    if hand:
        for card in range(n):
            # get a list of cards available to this player
            available_cards = Card.objects.filter(in_freeversion=True)
            # select a random card and add it to the hand
            card = random.choice(available_cards)
            hand = Hand_card(card=card)
            hand.save()
    print('players new hand:')
    print(current_player)
