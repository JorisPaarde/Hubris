from django.shortcuts import render
from .models import Player_type

# Create your views here.


def player_select(request):
    """view to return player selection page"""

    player_type = Player_type.objects.all()

    context = {
        'player_type': player_type,
    }
    
    return render(request, 'profiles/player-select.html', context)


def game_setup(request, value):

    if request.method == 'POST':
        print(value)
        print(request.POST['player-select'])
    
    return render(request, 'battle/battle.html')