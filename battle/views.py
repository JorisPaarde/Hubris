from django.shortcuts import render
from .models import Player_type

# Create your views here.


def battle_screen(request):
    """view to return battle_screen page"""

    player_type = Player_type.objects.all()

    context = {
        'player_type': player_type,
    }

    return render(request, 'battle/battle.html', context)
