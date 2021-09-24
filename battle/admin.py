from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Enemy)
admin.site.register(Game)
admin.site.register(Current_game_floor)
admin.site.register(Game_floor_enemy)
