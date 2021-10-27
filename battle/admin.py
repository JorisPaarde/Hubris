from django.contrib import admin
from .models import Enemy, Game, Current_game_floor, Game_floor_enemy
# Register your models here.


class EnemyyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'in_freeversion',
        'image_idle',
        'image_die',
    )


class GameAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'completed',
        'score',
        'total_gamefloors_played',
    )


admin.site.register(Enemy, EnemyyAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Current_game_floor)
admin.site.register(Game_floor_enemy)
