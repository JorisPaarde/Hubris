"""
Profiles App - Utilitys
----------------
various utilities for Profiles app views.
    - draw_cards
    - reset_player_stats
"""

import random

from django.contrib.auth.models import User

from .models import Card
from .models import HandCard


def draw_cards(number_of_cards, current_player):
    """function to draw new cards for a hand"""
    for card in range(number_of_cards):
        # get a list of cards available to this player
        available_cards = Card.objects.filter(in_freeversion=True)
        # if full version is payed all enemies are available
        current_user = User.objects.get(username=current_player.user)
        if current_user.profile.payed_full_version:
            available_cards = Card.objects.all()
        # select a random card and add it to the hand
        card = random.choice(available_cards)
        card = HandCard(card=card)
        card.save()
        current_player.hand.add(card)
        current_player.save()


def reset_player_stats(player):
    """ Function to reset player stats """
    player.type = None
    player.fire_attack_power = 0
    player.fire_defense = 0
    player.ice_attack_power = 0
    player.ice_defense = 0
    player.drain_attack_power = 0
    player.drain_defense = 0
    player.lightning_attack_power = 0
    player.lightning_defense = 0
    player.golem_attack_power = 0
    player.physical_defense = 0
    player.healing_power = 0
    player.mana_current = 0
    player.mana_max = 0
    player.health_current = 0
    player.health_max = 0
    player.save()
