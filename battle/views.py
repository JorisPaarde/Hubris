"""
Battle App - Views
----------------
Views for Battle app:
    - Battle_screen
    - Card_select
    - Proceed_to_next_floor
    - Next_floor_start
Function to handle enemy attacks:
    - enemy_attack_processor
"""


import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned

from profiles.models import Card
from profiles.utils import draw_cards
from profiles.models import HandCard

from .models import Player
from .models import Game
from .models import CurrentGameFloor
from .models import Enemy
from .models import GameFloorEnemy
from .utils import action_processor
from .utils import attack_target
from .utils import heal_target
from .utils import check_dead_monsters
from .utils import pickmonsters


@login_required(login_url='home:login')
def battle_screen(request, game):
    """view to return battle_screen page"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    cards = Card.objects.all()
    # logic to prevent having two unfinished games open at the same time
    try:
        game = Game.objects.get(player=player, completed=False)
    except MultipleObjectsReturned:
        game = Game.objects.filter(player=player).earliest('date_time_created')
        game.completed = True
        game.save()
        game = Game.objects.get(player=player, completed=False)

    current_game_floor = CurrentGameFloor.objects.get(
        pk=game.current_game_floor.pk)
    enemies = Enemy.objects.all()

    # card playing phase
    if game.game_step == '1':
        # shows cards to play and continues to the battle at step 2
        messages.info(request, "Please select a card to play.")

    # monster battle phase
    if game.game_step == '2':

        # select monster(s) from database
        # if there are no enemy's in this gamefloor
        if len(current_game_floor.enemy.all()) == 0:
            pickmonsters(request, game)

        # pass post requests from action.js to correct function
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            request_data = json.load(request)['post_data']
            if 'action' in request_data:
                action_processor(request, request_data)
            if 'all_enemies_dead' in request_data:
                check_dead_monsters(request)
                return redirect('battle:proceed_to_next_floor')
            if 'enemy_action' in request_data:
                enemy_attack_processor(request, request_data)

    context = {
        "game": game,
        "current_game_floor": current_game_floor,
        "player": player,
        "cards": cards,
        "enemies": enemies,
    }

    return render(request, 'battle/battle.html', context)


@login_required(login_url='home:login')
def card_select(request, card):
    """view to handle card selection and return to the next game step"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player, completed=False)

    if request.method == 'POST':
        played_hand_card = HandCard.objects.get(pk=card)
        if game.game_step == '1':
            # get the card and update the players stats
            played_card = Card.objects.get(title=played_hand_card)
            attack_modifier = played_card.attack_modifier
            healing_modifier = played_card.healing_modifier
            defence_modifier = played_card.defence_modifier
            health_modifier = played_card.health_modifier
            mana_modifier = played_card.mana_modifier
            skill = played_card.get_skill_style_display().lower()

            if skill == 'lightning':
                player.lightning_attack_power = min(
                    99, player.lightning_attack_power + attack_modifier)
                player.lightning_defense = min(
                    99, player.lightning_defense + defence_modifier)
            if skill == 'fire':
                player.fire_attack_power = min(
                    99, player.fire_attack_power + attack_modifier)
                player.fire_defense = min(
                    99, player.fire_defense + defence_modifier)
            if skill == 'golem':
                player.golem_attack_power = min(
                    99, player.golem_attack_power + attack_modifier)
                player.physical_defense = min(
                    99,  player.physical_defense + defence_modifier)
            if skill == 'ice':
                player.ice_attack_power = min(
                    99, player.ice_attack_power + attack_modifier)
                player.ice_defense = min(
                    99, player.ice_defense + defence_modifier)
            if skill == 'drain':
                player.drain_attack_power = min(
                    99, player.drain_attack_power + attack_modifier)
                player.drain_defense = min(
                    99, player.drain_defense + defence_modifier)
            if skill == 'heal':
                player.healing_power = min(
                    99, player.healing_power + healing_modifier)
                player.health_max = min(
                    99, player.health_max + health_modifier)
                player.health_current = player.health_max
            if skill == 'mana':
                player.mana_max = min(99, player.mana_max + mana_modifier)
                player.mana_current = player.mana_max

            player.hand.remove(card)
            player.save()
            played_hand_card.delete()

            # set game step to 2
            game.game_step = '2'
            game.save()

        if game.game_step == '3':
            # this is the discard phase of the game
            # remove the selected card from the players hand
            #  and the hand card itself
            player.hand.remove(card)
            player.save()
            played_hand_card.delete()
            # draw new cards for this player
            number_cards_in_hand = len(player.hand.all())
            draw_cards((8-number_cards_in_hand), player)
            # player is send to page where
            # he/she decides to go up a level or not
            return redirect('battle:proceed_to_next_floor')
    else:
        messages.info(request, "u already selected a spell")

    return redirect('battle:battle-screen', game)


@login_required(login_url='home:login')
def proceed_to_next_floor(request):
    """
    view to return huberis game step page
    In this view the player discards a card,
    and decides if he/she wants to go up a level.
    """
    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player, completed=False)
    current_game_floor = CurrentGameFloor.objects.get(
        pk=game.current_game_floor.pk)
    # if the game is not finished yet
    if game.current_game_floor_number != 15:
        cards = Card.objects.all()
        messages.info(request, "Please select a card to discard")
    #  if the game is finished:
    if game.current_game_floor_number == 15:
        game.completed = True
        game.save()
        # delete gamefloor
        current_game_floor.delete()
        # redirect to victory score page
        return redirect("home:leaderboard")
    context = {
        "game": game,
        "player": player,
        "cards": cards,
        "current_game_floor": current_game_floor,
    }

    return render(request,
                  'battle/proceed/proceed-to-next-floor.html', context)


@login_required(login_url='home:login')
def next_floor_start(request, choice):
    """
    view to set up the game for a new level,
    and control if a player goes up a level.
    """
    current_user = request.user
    player = Player.objects.get(user=current_user)
    # create a new empty gamefloor
    game = Game.objects.get(player=player, completed=False)
    next_game_floor = CurrentGameFloor()
    next_game_floor.save()
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
    # player completed a floor
    game.total_gamefloors_played = game.total_gamefloors_played + 1
    player.save()

    if request.method == 'POST':
        if 'level-select' in request.POST:
            if choice == 'y':
                # start game at next floor number
                game.current_game_floor_number = game.current_game_floor_number + 1
                game.save()
            else:
                pass
            # start game at the current floor number
            return redirect('battle:battle-screen', game)


def enemy_attack_processor(request, request_data):
    """
    Function to handle enemy attacks on player
    """
    # get the attacker and its values
    enemy_id = request_data['enemy']
    attacker = GameFloorEnemy.objects.get(id=enemy_id)
    attack_style = attacker.skill_style
    attack_power = attacker.attack_power
    # set has attacked to true
    attacker.has_attacked = True
    attacker.save()
    # get the target and its values
    current_user = request.user
    player = Player.objects.get(user=current_user)
    fire_defense = player.fire_defense
    ice_defense = player.ice_defense
    golem_defense = player.physical_defense
    lightning_defense = player.lightning_defense
    drain_defense = player.drain_defense
    target_player = Player.objects.filter(user=current_user)
    # calculate amount of damage done to player by this enemy
    if attack_style == 'DR':
        attack_power = max(0, attack_power - drain_defense)
        # enemy gets healed by the amount of damage it does
        heal_target(attacker, attack_power)
    if attack_style == 'LN':
        attack_power = max(0, attack_power - lightning_defense)
    if attack_style == 'FR':
        attack_power = max(0, attack_power - fire_defense)
    if attack_style == 'IC':
        attack_power = max(0, attack_power - ice_defense)
    if attack_style == 'GL':
        attack_power = max(0, attack_power - golem_defense)

    damage = attack_power
    attack_target(request, target_player, damage)
