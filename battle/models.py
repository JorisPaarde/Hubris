from django.db import models
from profiles.models import Player, Player_type
from django.conf import settings

# Create your models here.


class Enemy(models.Model):

    in_fullversion = models.BooleanField(default=True)
    name = models.CharField(max_length=254)
    image_idle = models.ImageField(null=True, blank=True)
    image_idle_url = models.URLField(null=True, blank=True)
    image_attack = models.ImageField(null=True, blank=True)
    image_attack_url = models.URLField(null=True, blank=True)
    image_die = models.ImageField(null=True, blank=True)
    image_die_url = models.URLField(null=True, blank=True)
    max_health = models.IntegerField(default=0)
    attack_power = models.IntegerField(default=0)
    skill_style = models.CharField(max_length=2, choices=settings.SKILL_STYLES)
    attack_phase = models.CharField(max_length=1, choices=settings.ATTACK_PHASES)
    xp_value = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Game(models.Model):

    date_time_created = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.BigIntegerField(default=0)
    game_step = models.CharField(max_length=1, choices=settings.GAME_STEPS)

    def __str__(self):
        return str(self.id)


class Current_game_floor(models.Model):

    date_time_created = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    current_phase = models.CharField(max_length=1, choices=settings.ATTACK_PHASES)

    def __str__(self):
        return str(self.id)


class Game_floor_enemy(models.Model):

    health_current = models.IntegerField(null=True, blank=True)
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)
    game_floor = models.ForeignKey(Current_game_floor,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)