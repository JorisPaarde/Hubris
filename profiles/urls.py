from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('player_select/', views.player_select, name='player_select'),
    path('continue_game/<continue_game>', views.continue_game,
         name='continue_game'),
    path('game_setup/<selected>', views.game_setup, name='game_setup'),
    path('player-death', views.player_death, name='player-death'),
]
