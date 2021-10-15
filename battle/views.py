import json
import random
import time

from django.shortcuts import render, redirect
from .models import Player, Game, Current_game_floor, Enemy, Game_floor_enemy
from profiles.models import Card
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

# Create your views here.


def battle_screen(request, game):
    """view to return battle_screen page"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    cards = Card.objects.all()
    game = Game.objects.get(player=player)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)
    enemies = Enemy.objects.all()

    # card playing phase
    if game.game_step == '1':
        messages.info(request, "Please select a card to play.")

    # monster battle phase
    if game.game_step == '2':

        # select monster(s) from database if there are none
        if len(Game_floor_enemy.objects.all()) == 0:
            pickmonsters(request, game)

        # pass post requests from action.js to correct function
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            request_data = json.load(request)['post_data']
            print(request_data)
            if 'action' in request_data:
                action_processor(request, request_data)
            if 'all_enemies_dead' in request_data:
                print(request)
                print("do shite because the're dead")
                check_dead_monsters(request)

    context = {
        "game": game,
        "current_game_floor": current_game_floor,
        "player": player,
        "cards": cards,
        "enemies": enemies,
    }

    return render(request, 'battle/battle.html', context)


def card_select(request, card):
    """function to handle card selection and return to the next game step"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player)

    if game.game_step == '1':

        if request.method == 'POST':
            # get the card and update the players stats
            card = Card.objects.get(pk=card)

            attack_modifier = card.attack_modifier
            healing_modifier = card.healing_modifier
            defence_modifier = card.defence_modifier
            skill = card.get_skill_style_display().lower()

            if skill == 'lightning':
                player.lightning_attack_power = player.lightning_attack_power + attack_modifier
                player.lightning_defense = player.lightning_defense + defence_modifier
                player.save()
            if skill == 'fire':
                player.fire_attack_power = player.fire_attack_power + attack_modifier
                player.fire_defense = player.fire_defense + defence_modifier
                player.save()
            if skill == 'golem':
                player.golem_attack_power = player.golem_attack_power + attack_modifier
                player.physical_defense = player.physical_defense + defence_modifier
                player.save()
            if skill == 'ice':
                player.ice_attack_power = player.ice_attack_power + attack_modifier
                player.ice_defense = player.ice_defense + defence_modifier
                player.save()
            if skill == 'drain':
                player.drain_attack_power = player.drain_attack_power + attack_modifier
                player.drain_defense = player.drain_defense + defence_modifier
                player.save()
            if skill == 'healing':
                player.healing_power = player.healing_power + healing_modifier
                player.save()

            # set game step to 2
            game.game_step = '2'
            game.save()

    else:
        messages.info(request, "u already selected a spell")

    return redirect('battle:battle-screen', game)


def attack_target(targets, damage):
    """function to handle target attacks"""
    for target in targets:
        target.health_current = target.health_current - damage
        # prevent negative health
        target.health_current = max(0, target.health_current)
        target.save()


def heal_player(player, amount):
    """function to handle player healing"""
    player.health_current = player.health_current + amount
    if player.health_current > player.health_max:
        player.health_current = player.health_max
    player.save()


def spend_mana(player, amount):
    """function to handle mana spending"""
    player.mana_current = player.mana_current - amount
    player.save()


def action_processor(request, request_data):
    """function to handle player actions"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player)
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
        heal_player(player, player.healing_power)
        spend_mana(player, player.healing_cost)

    if action == 'ice':
        attack_target(targets, player.ice_attack_power)
        spend_mana(player, player.ice_attack_cost)

    if action == 'golem':
        attack_target(target, player.golem_attack_power)
        spend_mana(player, player.golem_attack_cost)

    if action == 'fire':
        attack_target(target, player.fire_attack_power)
        spend_mana(player, player.fire_attack_cost)

    if action == 'lightning':
        attack_target(target, player.lightning_attack_power)
        spend_mana(player, player.lightning_attack_cost)

    if action == 'drain':
        enemy = current_game_floor.enemy.get(pk=selected_enemy)
        # player can only heal to the amount of damge done
        if player.drain_attack_power > enemy.health_current:
            amount = enemy.health_current
        else:
            amount = player.drain_attack_power
        heal_player(player, amount)
        attack_target(target, player.drain_attack_power)
        spend_mana(player, player.drain_attack_cost)

    skip_to_next_phase(current_game_floor)


def pickmonsters(request, game):
    """function to ramndomly select monsters from the database"""
    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    # determine the amount of enemies
    number_of_enemies = 2
    floor_nr = game.completed_game_floors
    # if floor_nr % 2 == 0:
    #     number_of_enemies = 2
    # if floor_nr % 3 == 0:
    #     number_of_enemies = 3

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

            max_health = max(rand_int_1, rand_int_2)/number_of_enemies
            attack_power = min(rand_int_1, rand_int_2)/number_of_enemies

            health_current = max_health
            skill_style = random.choice(settings.SKILL_STYLES)[1]
            # while loop to prevent enemy skill to be heal
            while skill_style.lower() == 'heal':
                skill_style = random.choice(settings.SKILL_STYLES)[1]
            attack_phase = random.choice(settings.ATTACK_PHASES)[1]

            game_floor_enemy = Game_floor_enemy(
                                                enemy=random_enemy,
                                                health_current=health_current,
                                                max_health=max_health,
                                                attack_power=attack_power,
                                                skill_style=skill_style,
                                                attack_phase=attack_phase
                                                )

            game_floor_enemy.save()
            current_game_floor.enemy.add(game_floor_enemy)
            current_game_floor.save()


def skip_to_next_phase(current_game_floor):
    """function to skip to the next phase as long as there is a next one"""
    n = int(current_game_floor.current_phase)
    if n >= len(settings.ATTACK_PHASES):
        pass
    else:
        n += 1
        str(n)
        current_game_floor.current_phase = n
        current_game_floor.save()


def check_dead_monsters(request):
    """ function to check in the database if all monsters are indeed dead,
    if so delete data from this level to make room for a next one"""
    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    # if all enemies are dead now u win the round
    killed = 0
    for enemy in current_game_floor.enemy.all():

        if enemy.health_current == 0:
            killed += 1

    if killed == len(current_game_floor.enemy.all()):
        for enemy in current_game_floor.enemy.all():
            enemy.delete()
        game.completed_game_floors = game.completed_game_floors + 1
        game.game_step = '3'
        # create a new gamefloor
        new_game_floor = Current_game_floor()
        new_game_floor.save()
        game.current_game_floor = new_game_floor
        game.save()

