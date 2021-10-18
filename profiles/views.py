from django.shortcuts import render, redirect, get_object_or_404
from .models import Player_type, Player, Card, Hand_card
from battle.models import Game, Current_game_floor
from django.contrib import messages


import random
# Create your views here.


def player_select(request):
    """view to return player selection page"""

    current_user = request.user
    current_player = Player.objects.filter(user=current_user)

    if not current_player:
        current_player = Player(user=current_user)
        current_player.save()

    # collect all player types
    player_type = Player_type.objects.all()
    context = {
        'player_type': player_type,
    }

    # check if this user already has a player (with an unfinished game)
    if current_player:
        current_player = get_object_or_404(Player, user=current_user)
        current_game = Game.objects.filter(player=current_player, completed=False)
        # if there is an unfinished game send it to the template
        if current_game:

            current_game = get_object_or_404(Game, player=current_player, completed=False)

            if not current_game.completed:
                context.update({'game': current_game})
                messages.info(
                    request, f"{current_user} do you want to continue your current game?")

    return render(request, 'profiles/player-select.html', context)


def continue_game(request, continue_game):
    """view to return player to current game or start a new game"""

    # get current player
    current_user = request.user
    current_player = Player.objects.get(user=current_user)

    if continue_game == 'y':

        game = Game.objects.get(player=current_player)
        context = {
            'game': game,
        }

        return redirect('battle:battle-screen', context)

    else:
        # set current game to completed and return to selection screen.
        current_game = Game.objects.get(player=current_player, completed=False)
        current_game.completed = True
        current_game.save()
        current_game_floor = Current_game_floor.objects.get(pk=current_game.current_game_floor.pk)
        # delete all cards and enemies from this game
        current_game_floor.enemy.all().delete()
        current_game_floor.delete()
        current_player.hand.all().delete()
        current_player.delete()

        return redirect('profiles:player_select')


def game_setup(request, selected):

    if request.method == 'POST':

        context = {}
        # check if this user already has a player
        current_user = request.user
        current_player_resultset = Player.objects.filter(user=current_user)
        # get the selected player type

        selected_type = Player_type.objects.get(selected=selected)
        # if not, create a new player and set the initial values for that player
        if not current_player_resultset:
            # create a player for the current user
            current_player = Player(user=current_user, type=selected_type)
            current_player.save()
        else:
            current_player = Player.objects.get(user=current_user)

        # create an empty hand for this player
        current_player.hand.clear()
        # add cards to this hand
        draw_n_cards = 8
        draw_cards(draw_n_cards, current_player)

        # create a new game for this player and a first game floor
        game_floor = Current_game_floor()
        game_floor.save()
        game = Game(player=current_player, current_game_floor=game_floor)
        game.save()
        context.update({'game': game})

        if str(selected_type):
            # values set for fire wizard
            if str(selected_type) == 'FR':
                current_player = Player(pk=current_player.id,
                                        type=selected_type,
                                        user=current_user,
                                        fire_attack_power=3,
                                        fire_defense=3,
                                        mana_max=4,
                                        mana_current=4,
                                        health_max=6,
                                        health_current=6
                                        )
                current_player.save()
            # values set for lightning wizard
            elif str(selected_type) == 'LN':
                current_player = Player(pk=current_player.id,
                                        type=selected_type,
                                        user=current_user,
                                        lightning_attack_power=2,
                                        lightning_defense=3,
                                        mana_max=4,
                                        mana_current=4,
                                        health_max=6,
                                        health_current=6
                                        )
                current_player.save()
            # values set for ice wizard
            elif str(selected_type) == 'IC':
                current_player = Player(pk=current_player.id,
                                        type=selected_type,
                                        user=current_user,
                                        ice_attack_power=100,
                                        ice_defense=3,
                                        mana_max=4,
                                        mana_current=4,
                                        health_max=6,
                                        health_current=6
                                        )
                current_player.save()
    # start this users game with this player

    return redirect('battle:battle-screen', context)


# function to draw new cards for a hand
def draw_cards(n, current_player):
    for card in range(n):
        # get a list of cards available to this player
        available_cards = Card.objects.filter(in_freeversion=True)
        # select a random card and add it to the hand
        card = random.choice(available_cards)
        card = Hand_card(card=card)
        card.save()
        current_player.hand.add(card)
        current_player.save()
