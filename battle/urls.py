from django.urls import path
from . import views

app_name = "battle"

urlpatterns = [
    path('', views.battle_screen, name='battle-screen'),
    path('<game>', views.battle_screen, name='battle-screen'), 
    path('card_select/<card>', views.card_select, name='card-select'),
    path('action_processor', views.action_processor, name='action_processor'),
    path('proceed-to-next-floor/', views.proceed_to_next_floor, name='proceed_to_next_floor'),
    path('next-floor-start/<choice>', views.next_floor_start, name='next-floor-start'),
    path('player-death', views.player_death, name='player-death'),
]
