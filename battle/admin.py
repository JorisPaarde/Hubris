"""
Battle app admin models
-------------------------
Classes for Battle app:
    - EnemyAdmin
    - GameAdmin
"""

from django.contrib import admin
from .models import Enemy
from .models import Game
from .models import CurrentGameFloor
from .models import GameFloorEnemy
# Register your models here.


class EnemyAdmin(admin.ModelAdmin):
    """ class to adjust enemy admin display values """
    list_display = (
        'name',
        'in_freeversion',
        'image_idle',
        'image_die',
    )


class GameAdmin(admin.ModelAdmin):
    """ class to adjust game admin display values """
    list_display = (
        'pk',
        'completed',
        'score',
        'total_gamefloors_played',
    )


admin.site.register(Enemy, EnemyAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(CurrentGameFloor)
admin.site.register(GameFloorEnemy)
