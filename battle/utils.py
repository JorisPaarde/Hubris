import random
import time

from django.conf import settings
from django.shortcuts import redirect
from .models import Player
from .models import Game
from .models import Current_game_floor
from .models import Enemy
from .models import Game_floor_enemy


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
    current_game_floor = Current_game_floor.objects.get(
        pk=game.current_game_floor.pk)

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
        attack_target(request, target, player.golem_attack_power)
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
    current_game_floor = Current_game_floor.objects.get(
        pk=game.current_game_floor.pk)

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
            # if full version is payed all enemies are available
            if current_user.profile.payed_full_version:
                available_enemies = Enemy.objects.all()
            # select a random enemy and add it to the game_floor
            random_enemy = random.choice(available_enemies)
            # determine the stats for this enemy
            random.seed(time.process_time())
            rand_int_1 = random.randint(1, floor_nr * 3) + floor_nr
            random.seed(time.process_time())
            rand_int_2 = max(3, random.randint(1, rand_int_1))

            health_max = max(
                rand_int_1, rand_int_2)/number_of_enemies + floor_nr
            attack_power = min(
                rand_int_1, rand_int_2)/number_of_enemies + floor_nr

            health_current = health_max
            skill_style = random.choice(settings.ENEMY_SKILL_STYLES)[0]
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
        if not check_dead_monsters(request):
            # if they are not,player failed, kill player
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
    current_game_floor = Current_game_floor.objects.get(
        pk=game.current_game_floor.pk)

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
        return True
    else:
        # return they are not all dead
        return False
