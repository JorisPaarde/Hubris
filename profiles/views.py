from django.shortcuts import render
from .models import Player_type, Hand_card, Player, Card

# Create your views here.


def player_select(request):
    """view to return player selection page"""

    player_type = Player_type.objects.all()

    context = {
        'player_type': player_type,
    }
    
    return render(request, 'profiles/player-select.html', context)


def game_setup(request, selected):

    if request.method == 'POST':
        # create a hand with cards for this player
        hand = Hand_card.objects.all()
        print(hand)
        # card to add to hand
        card1 = Card.objects.get(pk=1)
        # add card to hand
        hand.add(card1)
        print(hand)
        # create a new player and set the initial values for that player


        # connect this player to the current user
    
    return render(request, 'battle/battle.html')