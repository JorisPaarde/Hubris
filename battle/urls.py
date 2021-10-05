from django.urls import path
from . import views

app_name = "battle"

urlpatterns = [
    path('', views.battle_screen, name='battle-screen'),
    path('<game>', views.battle_screen, name='battle-screen'),
    path('card_select/<card>', views.card_select, name='card-select'),
]
