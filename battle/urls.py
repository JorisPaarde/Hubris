from django.urls import path
from . import views
from . import utils

app_name = "battle"

urlpatterns = [
    path('', views.battle_screen, name='battle-screen'),
    path('<game>', views.battle_screen, name='battle-screen'),
    path('card_select/<card>', views.card_select, name='card-select'),
    path('proceed-to-next-floor/', views.proceed_to_next_floor, name='proceed_to_next_floor'),
    path('next-floor-start/<choice>', views.next_floor_start, name='next-floor-start'),
]
