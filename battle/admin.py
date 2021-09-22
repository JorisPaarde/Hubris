from django.contrib import admin
from .models import Card, Enemy
# Register your models here.


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    pass
