from django.db import models
from profiles.models import Player, Player_type
from django.conf import settings

# Create your models here.


class Enemy(models.Model):

    in_freeversion = models.BooleanField(default=True)
    name = models.CharField(max_length=254)
    image_idle = models.ImageField(null=True, blank=True)
    image_idle_url = models.URLField(null=True, blank=True)
    image_attack = models.ImageField(null=True, blank=True)
    image_attack_url = models.URLField(null=True, blank=True)
    image_die = models.ImageField(null=True, blank=True)
    image_die_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Game_floor_enemy(models.Model):

    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE, null=True, blank=True)
    max_health = models.IntegerField(default=0)
    health_current = models.IntegerField(null=True)
    attack_power = models.IntegerField(default=0)
    skill_style = models.CharField(max_length=2, choices=settings.SKILL_STYLES, default=settings.SKILL_STYLES[0][0])
    attack_phase = models.CharField(max_length=1, choices=settings.ATTACK_PHASES, default=settings.ATTACK_PHASES[0][0])

    def __str__(self):
        return str(self.id)


class Current_game_floor(models.Model):

    date_time_created = models.DateTimeField(auto_now=True)
    current_phase = models.CharField(max_length=1, choices=settings.ATTACK_PHASES, default=settings.ATTACK_PHASES[0][0])
    enemy = models.ManyToManyField(Game_floor_enemy)

    def __str__(self):
        return str(self.id)


class Game(models.Model):

    date_time_created = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.BigIntegerField(default=0)
    game_step = models.CharField(max_length=1, choices=settings.GAME_STEPS, default=1)
    current_game_floor = models.ForeignKey(Current_game_floor, on_delete=models.SET_NULL, default=1, null=True)
    current_game_floor_number = models.IntegerField(default=1)
    total_gamefloors_played =  models.IntegerField(default=0)


    def __str__(self):
        return str(self.id)
