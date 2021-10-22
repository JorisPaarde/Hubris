from django.contrib import admin
from .models import Enemy, Game, Current_game_floor, Game_floor_enemy
# Register your models here.


class EnemyyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'in_freeversion',
    )

admin.site.register(Enemy, EnemyyAdmin)
admin.site.register(Game)
admin.site.register(Current_game_floor)
admin.site.register(Game_floor_enemy)
