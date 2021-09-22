from django.contrib import admin
from .models import Card, Enemy, Player_type
# Register your models here.


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(Enemy)
class EnemiesAdmin(admin.ModelAdmin):
    pass


@admin.register(Player_type)
class PlayerTypeAdmin(admin.ModelAdmin):
    pass
