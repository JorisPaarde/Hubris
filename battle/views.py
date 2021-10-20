import json
import random
import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from profiles.models import Card
from profiles.views import draw_cards
from .models import Player, Game, Current_game_floor, Enemy, Game_floor_enemy, Hand_card


# Create your views here.

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

    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)
    enemies = Enemy.objects.all()

    # card playing phase
    if game.game_step == '1':
        # shows cards to play and continues to the battle at step 2
        messages.info(request, "Please select a card to play.")

    # monster battle phase
    if game.game_step == '2':

        # select monster(s) from database if there are no enemy's in this gamefloor
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
    """function to handle card selection and return to the next game step"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player, completed=False)

    if request.method == 'POST':
        played_hand_card = Hand_card.objects.get(pk=card)
        if game.game_step == '1':
            # get the card and update the players stats
            played_card = Card.objects.get(title=played_hand_card)
            attack_modifier = played_card.attack_modifier
            healing_modifier = played_card.healing_modifier
            defence_modifier = played_card.defence_modifier
            skill = played_card.get_skill_style_display().lower()

            if skill == 'lightning':
                player.lightning_attack_power = min(99, player.lightning_attack_power + attack_modifier)
                player.lightning_defense = min(99, player.lightning_defense + defence_modifier)
            if skill == 'fire':
                player.fire_attack_power = min(99, player.fire_attack_power + attack_modifier)
                player.fire_defense = min(99, player.fire_defense + defence_modifier)
            if skill == 'golem':
                player.golem_attack_power = min(99, player.golem_attack_power + attack_modifier)
                player.physical_defense = min(99,  player.physical_defense + defence_modifier)
            if skill == 'ice':
                player.ice_attack_power = min(99, player.ice_attack_power + attack_modifier)
                player.ice_defense = min(99, player.ice_defense + defence_modifier)
            if skill == 'drain':
                player.drain_attack_power = min(99, player.drain_attack_power + attack_modifier)
                player.drain_defense = min(99, player.drain_defense + defence_modifier)
            if skill == 'healing':
                player.healing_power = min(99, player.healing_power + healing_modifier)

            player.hand.remove(card)
            player.save()
            played_hand_card.delete()

            # set game step to 2
            game.game_step = '2'
            game.save()

        if game.game_step == '3':
            # this is the discard phase of the game
            # remove the selected card from the players hand and the hand card itself
            player.hand.remove(card)
            player.save()
            played_hand_card.delete()
            # draw new cards for this player
            number_cards_in_hand = len(player.hand.all())
            draw_cards((8-number_cards_in_hand), player)
            # player is send to page where he/she decides to go up a level or not
            return redirect('battle:proceed_to_next_floor')
    else:
        messages.info(request, "u already selected a spell")

    return redirect('battle:battle-screen', game)


def attack_target(request, targets, damage):
    """function to handle target attacks"""
    for target in targets:
        target.health_current = target.health_current - damage
        # prevent negative health
        target.health_current = max(0, target.health_current)
        target.save()
        if hasattr(target, 'enemy'):
            if target.health_current == 0:
                # this enemy died score it
                score(request, target)


def score(request, enemy):
    """function to score enemy kills"""
    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player, completed=False)
    new_score = enemy.attack_power + enemy.health_max
    game.score = game.score + new_score
    game.save()


def heal_target(target, amount):
    """function to handle player healing"""
    target.health_current = target.health_current + amount
    if target.health_current > target.health_max:
        target.health_current = target.health_max
    target.save()


def spend_mana(player, amount):
    """function to handle mana spending"""
    player.mana_current = player.mana_current - amount
    player.save()


def action_processor(request, request_data):
    """function to handle player actions"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player, completed=False)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    # logic for getting the player action with corresponding enemy target,
    # and sending it to the action processor

    action_selection = request_data
    action = action_selection['action']

    if action_selection['enemy'] != 'notspecified':
        selected_enemy = action_selection['enemy']
        target = current_game_floor.enemy.filter(pk=selected_enemy)

    targets = current_game_floor.enemy.all()
    if action == 'skip':
        pass

    if action == 'healing':
        heal_target(player, player.healing_power)
        spend_mana(player, player.healing_cost)

    if action == 'ice':
        attack_target(request, targets, player.ice_attack_power)
        spend_mana(player, player.ice_attack_cost)

    if action == 'golem':
        attack_target(request,target, player.golem_attack_power)
        spend_mana(player, player.golem_attack_cost)

    if action == 'fire':
        attack_target(request, target, player.fire_attack_power)
        spend_mana(player, player.fire_attack_cost)

    if action == 'lightning':
        attack_target(request, target, player.lightning_attack_power)
        spend_mana(player, player.lightning_attack_cost)

    if action == 'drain':
        enemy = current_game_floor.enemy.get(pk=selected_enemy)
        # player can only heal to the amount of damge done
        if player.drain_attack_power > enemy.health_current:
            amount = enemy.health_current
        else:
            amount = player.drain_attack_power
        heal_target(player, amount)
        attack_target(request, target, player.drain_attack_power)
        spend_mana(player, player.drain_attack_cost)

    skip_to_next_phase(request, current_game_floor)


def pickmonsters(request, game):
    """function to ramndomly select monsters from the database"""
    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player, completed=False)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    # determine the amount of enemies
    number_of_enemies = 1
    floor_nr = game.current_game_floor_number
    if floor_nr % 2 == 0:
        number_of_enemies = 2
    if floor_nr % 3 == 0:
        number_of_enemies = 3

    if current_game_floor:
        for game_floor_enemy in range(number_of_enemies):
            # get a list of enemies available to this player
            available_enemies = Enemy.objects.filter(in_freeversion=True)
            # select a random enemy and add it to the game_floor
            random_enemy = random.choice(available_enemies)
            # determine the stats for this enemy
            random.seed(time.process_time())
            rand_int_1 = random.randint(3, floor_nr * 3)
            random.seed(time.process_time())
            rand_int_2 = max(4, random.randint(1, rand_int_1))

            health_max = max(rand_int_1, rand_int_2)/number_of_enemies + floor_nr
            attack_power = min(rand_int_1, rand_int_2)/number_of_enemies + floor_nr

            health_current = health_max
            skill_style = random.choice(settings.SKILL_STYLES)[0]
            # while loop to prevent enemy skill to be heal
            while skill_style.lower() == 'hl':
                skill_style = random.choice(settings.SKILL_STYLES)[0]
            attack_phase = random.choice(settings.ATTACK_PHASES)[0]
            game_floor_enemy = Game_floor_enemy(
                                                enemy=random_enemy,
                                                health_current=health_current,
                                                health_max=health_max,
                                                attack_power=attack_power,
                                                skill_style=skill_style,
                                                attack_phase=attack_phase
                                                )

            game_floor_enemy.save()
            current_game_floor.enemy.add(game_floor_enemy)
            current_game_floor.save()


def skip_to_next_phase(request, current_game_floor):
    """function to skip to the next phase as long as there is a next one"""
    current_user = request.user
    player = Player.objects.get(user=current_user)
    phase = int(current_game_floor.current_phase)
    # if this is the last phase
    if phase == len(settings.ATTACK_PHASES):
        # check if all enemies are dead
        # if they are not,player failed, kill player
        if not check_dead_monsters(request):
            player.health_current = 0
            player.save()
    else:
        phase += 1
        str(phase)
        current_game_floor.current_phase = phase
        current_game_floor.save()


def check_dead_monsters(request):
    """
    Function to check in the database if all monsters are indeed dead,
    if so delete data from this level and make a next one.
    """
    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player, completed=False)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    # if all enemies are dead now u win the round
    killed = 0
    for enemy in current_game_floor.enemy.all():

        if enemy.health_current == 0:
            killed += 1

    if killed == len(current_game_floor.enemy.all()):

        for enemy in current_game_floor.enemy.all():
            enemy.delete()
        game.game_step = '3'
        game.save()
    else:
        # return they are not all dead
        return False


@login_required(login_url='home:login')
def proceed_to_next_floor(request):
    """
    view to return huberis game step page
    In this view the player discards a card, and decides if he/she wants to go up a level.
    """
    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player, completed=False)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)
    # if the game is not finished yet
    if game.current_game_floor_number != 15:
        cards = Card.objects.all()
        messages.info(request, "Please select a card to discard")
    #  if the game is finished:
    if game.current_game_floor_number == 15:
        game.completed = True
        game.save()
        # redirect to victory score page
        return redirect("home:how-to-play")
    context = {
        "game": game,
        "player": player,
        "cards": cards,
        "current_game_floor": current_game_floor,
    }

    return render(request, 'battle/proceed/proceed-to-next-floor.html', context)


@login_required(login_url='home:login')
def next_floor_start(request, choice):
    """
    view to set up the game for a new level and control if a player goes up a level.
    """
    current_user = request.user
    player = Player.objects.get(user=current_user)
    # create a new empty gamefloor
    game = Game.objects.get(player=player, completed=False)
    next_game_floor = Current_game_floor()
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
    attacker = Game_floor_enemy.objects.get(id=enemy_id)
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
