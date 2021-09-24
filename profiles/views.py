from django.shortcuts import render

# Create your views here.


def player_select(request):
    """view to return player selection page"""

    return render(request, 'profiles/player-select.html')