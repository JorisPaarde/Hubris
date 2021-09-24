from django.shortcuts import render
from .models import Player_type

from forms import player_select_form
# Create your views here.


def player_select(request):
    """view to return player selection page"""

    selected = ''
    player_type = Player_type.objects.all()

    if request.method == 'POST':

        selected = request.POST.get()

    context = {
        'player_type': player_type,
        'selected': selected,
    }
    
    return render(request, 'profiles/player-select.html', context)