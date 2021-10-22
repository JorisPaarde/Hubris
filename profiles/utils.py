import random

from django.contrib.auth.models import User

from .models import Card, Hand_card


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
        card = Hand_card(card=card)
        card.save()
        current_player.hand.add(card)
        current_player.save()
