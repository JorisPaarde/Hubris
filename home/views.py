from django.shortcuts import render

# Create your views here.


def main_menu(request):
    """view to return main menu page"""

    return render(request, 'home/index.html')
