from django.urls import path
from . import views

app_name = "battle"

urlpatterns = [
    path('battle/', views.battle_screen, name='battle_screen'),
]
