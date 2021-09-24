from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('player_select/', views.player_select, name='player-select'),
]
