from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from battle.models import Game, Current_game_floor

from .models import Player_type
from .models import Player
from .utils import reset_player_stats
from .utils import draw_cards


@login_required(login_url='home:login')
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
        current_game = Game.objects.filter(
            player=current_player, completed=False)
        # if there is an unfinished game send it to the template
        if current_game:

            current_game = get_object_or_404(
                Game, player=current_player, completed=False)

            if not current_game.completed:
                context.update({'game': current_game})
                messages.info(
                    request,
                    f"{current_user} do you want to continue the current game?")

    return render(request, 'profiles/player-select.html', context)


@login_required(login_url='home:login')
def continue_game(request, continue_game):
    """view to return player to current game or start a new game"""

    # get current player
    current_user = request.user
    current_player = Player.objects.get(user=current_user)

    if continue_game == 'y':

        game = Game.objects.get(player=current_player, completed=False)
        context = {
            'game': game,
        }

        return redirect('battle:battle-screen', context)

    else:
        # set current game to completed and return to selection screen.
        current_game = Game.objects.get(player=current_player, completed=False)
        current_game.completed = True
        current_game.save()
        current_game_floor = Current_game_floor.objects.get(
            pk=current_game.current_game_floor.pk)
        # delete all cards and enemies from this game
        current_game_floor.enemy.all().delete()
        current_game_floor.delete()
        print(current_player.hand.all())
        current_player.hand.all().delete()
        reset_player_stats(current_player)
        return redirect('profiles:player_select')


@login_required(login_url='home:login')
def game_setup(request, selected):
    """view to process player selection and return the battle screen"""
    if request.method == 'POST':

        context = {}
        # check if this user already has a player
        current_user = request.user
        current_player_resultset = Player.objects.filter(user=current_user)
        # get the selected player type

        selected_type = Player_type.objects.get(selected=selected)
        # if not, create a new player
        # and set the initial values for that player
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
                                        fire_attack_power=6,
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
                                        lightning_attack_power=4,
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
                                        ice_attack_power=2,
                                        ice_defense=3,
                                        mana_max=4,
                                        mana_current=4,
                                        health_max=6,
                                        health_current=6
                                        )
                current_player.save()
    # start this users game with this player

    return redirect('battle:battle-screen', context)


@login_required(login_url='home:login')
def player_death(request):
    """
    view to set up the game for a new level and control player death.
    """
    current_user = request.user
    player = Player.objects.get(user=current_user)
    # check if the player is really dead
    if player.health_current == 0:

        # create a new empty gamefloor
        game = Game.objects.get(player=player, completed=False)
        next_game_floor = Current_game_floor()
        next_game_floor.save()
        # delete all enemys from this gamefloor
        for enemy in game.current_game_floor.enemy.all():
            enemy.delete()
        # delete the old gamefloor
        game.current_game_floor.delete()
        # add the new empty gamefloor to the game
        game.current_game_floor = next_game_floor
        # game starts at step 1 again
        game.game_step = '1'
        game.save()
        # player starts next floor with full stats
        player.health_current = player.health_max
        player.mana_current = player.mana_max
        # player played a floor
        game.total_gamefloors_played = game.total_gamefloors_played + 1
        player.save()
        # set game to previous floor number
        game.current_game_floor_number = max(
            1, game.current_game_floor_number - 1)
        game.save()
        # start game at the current floor number
    return redirect('battle:battle-screen', game)
