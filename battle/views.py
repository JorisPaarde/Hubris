from django.shortcuts import render
from .models import Player

# Create your views here.


def battle_screen(request):
    """view to return battle_screen page"""
    current_user = request.user
    player = Player.objects.get(user=current_user)

    context = {
        'player': player,
    }

    return render(request, 'battle/battle.html', context)
