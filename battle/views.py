from django.shortcuts import render

# Create your views here.


def battle_screen(request):
    """view to return battle_screen page"""

    return render(request, 'battle/battle.html')
