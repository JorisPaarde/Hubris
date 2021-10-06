from django.shortcuts import render, redirect
from .models import Player, Game, Current_game_floor, Enemy, Game_floor_enemy
from profiles.models import Card
from django.contrib import messages
from django.conf import settings

import random

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

    context = {
        "game": game,
        "current_game_floor": current_game_floor,
        "player": player,
        "cards": cards,
        "enemies": enemies,
    }

    return render(request, 'battle/battle.html', context)


def card_select(request, card):
    """view to handle card selection and return to the next game step"""

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


def monster_battle(request, action):

    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    print(action)

    if not action == 'skip' or 'heal':

        messages.info(request, "Select a target")

    if action == 'heal':
        player.health_current = player.health_current + player.healing_power
        if player.health_current > player.health_max:
            player.health_current = player.health_max
        player.save()

    if action == 'skip':
        # skip to the next phase as long as there is a next one
        n = int(current_game_floor.current_phase)
        if n >= len(settings.ATTACK_PHASES):
            pass
        else:
            n +=1
            str(n)
            current_game_floor.current_phase = n
            current_game_floor.save()

    return redirect('battle:battle-screen', game)


def pickmonsters(request, game):

    current_user = request.user
    player = Player.objects.get(user=current_user)
    game = Game.objects.get(player=player)
    current_game_floor = Current_game_floor.objects.get(pk=game.current_game_floor.pk)

    # determine the amount of enemies
    n = 3

    if current_game_floor:
        for game_floor_enemy in range(n):
            # get a list of enemies available to this player
            available_enemies = Enemy.objects.filter(in_freeversion=True)
            # select a random enemy and add it to the game_floor
            random_enemy = random.choice(available_enemies)
            game_floor_enemy = Game_floor_enemy(enemy=random_enemy)
            game_floor_enemy.save()
            current_game_floor.enemy.add(game_floor_enemy)
            current_game_floor.save()
