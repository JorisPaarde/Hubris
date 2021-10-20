import random

from .models import Card, Hand_card


def draw_cards(number_of_cards, current_player):
    """function to draw new cards for a hand"""
    for card in range(number_of_cards):
        # get a list of cards available to this player
        available_cards = Card.objects.filter(in_freeversion=True)
        # select a random card and add it to the hand
        card = random.choice(available_cards)
        card = Hand_card(card=card)
        card.save()
        current_player.hand.add(card)
        current_player.save()
