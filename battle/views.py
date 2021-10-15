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

        # pass post requests from action.js to action processor function
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            action_processor(request)

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

    print (targets)

    for target in targets:
        target.health_current = target.health_current - damage
        # prevent negative health
        target.health_current = max(0, target.health_current)
        target.save()


def heal_player(player, amount):

    player.health_current = player.health_current + amount
    if player.health_current > player.health_max:
        player.health_current = player.health_max
    player.save()


def action_processor(request):
    """view to handle player actions"""

    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    # logic for getting the player action with corresponding enemy target,
    # and sending it to the action processor

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        action_selection = json.load(request)['post_data']
        action = action_selection['action']

        if action_selection['enemy'] != 'notspecified':
            selected_enemy = action_selection['enemy']
            target = current_game_floor.enemy.filter(pk=selected_enemy)

        targets = current_game_floor.enemy.all()

    if action == 'healing':
        heal_player(player, player.healing_power)

    if action == 'skip':
        print('skip')
        # skip to the next phase as long as there is a next one
        skip_to_next_phase(current_game_floor)

    if action == 'ice':
        attack_target(targets, player.ice_attack_power)
        skip_to_next_phase(current_game_floor)

    if action == 'golem':
        attack_target(target, player.golem_attack_power)
        skip_to_next_phase(current_game_floor)

    if action == 'fire':
        attack_target(target, player.fire_attack_power)
        skip_to_next_phase(current_game_floor)

    if action == 'lightning':
        attack_target(target, player.lightning_attack_power)
        skip_to_next_phase(current_game_floor)

    if action == 'drain':
        heal_player(player, max([player.drain_attack_power,
                    target.health_current]))
        attack_target(target, player.drain_attack_power)
        skip_to_next_phase(current_game_floor)


    # if all enemies are dead now u win the round
    killed = 0
    for enemy in current_game_floor.enemy.all():

        if enemy.health_current == 0:
            killed += 1

    if killed == len(current_game_floor.enemy.all()):
        print('they all died')
        messages.info(request, "They all died.")


def pickmonsters(request, game):
    """function to ramndomly select monsters from the database"""
    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    # determine the amount of enemies
    n = 1
    floor_nr = game.completed_game_floors
    if floor_nr % 2 == 0:
        n = 2
    if floor_nr % 3 == 0:
        n = 3

    if current_game_floor:
        for game_floor_enemy in range(n):
            # get a list of enemies available to this player
            available_enemies = Enemy.objects.filter(in_freeversion=True)
            # select a random enemy and add it to the game_floor
            random_enemy = random.choice(available_enemies)
            # determine the stats for this enemy
            random.seed(time.process_time())
            rand_int_1 = random.randint(3, floor_nr * 3)
            random.seed(time.process_time())
            rand_int_2 = max(4, random.randint(1, rand_int_1))

            max_health = max(rand_int_1, rand_int_2)/n
            attack_power = min(rand_int_1, rand_int_2)/n

            health_current = max_health
            skill_style = random.choice(settings.SKILL_STYLES)[1]
            # while loop to prevent enemy skill to be heal
            while skill_style.lower() == 'heal':
                skill_style = random.choice(settings.SKILL_STYLES)[1]
            attack_phase = random.choice(settings.ATTACK_PHASES)[1]

            game_floor_enemy = Game_floor_enemy(
                                                enemy=random_enemy,
                                                health_current=health_current,
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
        n +=1
        str(n)
        current_game_floor.current_phase = n
        current_game_floor.save()
