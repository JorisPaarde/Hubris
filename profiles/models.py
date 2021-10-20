from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class Player_type(models.Model):

    selected = models.CharField(max_length=2, choices=settings.PLAYER_STYLES)
    image_idle = models.ImageField(null=True, blank=True)
    image_idle_url = models.URLField(null=True, blank=True)
    image_attack = models.ImageField(null=True, blank=True)
    image_attack_url = models.URLField(null=True, blank=True)
    image_die = models.ImageField(null=True, blank=True)
    image_die_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.selected


class Card(models.Model):

    in_freeversion = models.BooleanField(default=True)
    title = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    effect_text = models.CharField(max_length=254, null=True, blank=True)
    allowed_in_phase = models.CharField(max_length=4,
                                        choices=settings.ALLOWED_PHASES)
    attack_all = models.BooleanField(default=False)
    skill_style = models.CharField(max_length=2, choices=settings.SKILL_STYLES)
    attack_modifier = models.IntegerField(default=0)
    healing_modifier = models.IntegerField(default=0)
    defence_modifier = models.IntegerField(default=0)
    mana_cost = models.IntegerField(default=2)
    cards_discard_cost = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Hand_card(models.Model):

    date_time_created = models.DateTimeField(auto_now=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.card)


class Player(models.Model):

    date_time_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Player_type, on_delete=models.CASCADE, null=True)
    fire_attack_power = models.IntegerField(default=0)
    fire_defense = models.IntegerField(default=0)
    fire_attack_cost = models.IntegerField(default=4)
    fire_attack_phase = models.CharField(max_length=4,
                                        choices=settings.ALLOWED_PHASES, default='2')
    ice_attack_power = models.IntegerField(default=0)
    ice_defense = models.IntegerField(default=0)
    ice_attack_cost = models.IntegerField(default=2)
    ice_attack_phase = models.CharField(max_length=4,
                                        choices=settings.ALLOWED_PHASES, default='3')
    drain_attack_power = models.IntegerField(default=0)
    drain_defense = models.IntegerField(default=0)
    drain_attack_cost = models.IntegerField(default=1)
    drain_attack_phase = models.CharField(max_length=4,
                                        choices=settings.ALLOWED_PHASES, default='ALL')
    lightning_attack_power = models.IntegerField(default=0, validators=[])
    lightning_defense = models.IntegerField(default=0)
    lightning_attack_cost = models.IntegerField(default=2)
    lightning_attack_phase = models.CharField(max_length=4,
                                        choices=settings.ALLOWED_PHASES, default='1')
    golem_attack_power = models.IntegerField(default=0)
    physical_defense = models.IntegerField(default=0)
    golem_attack_cost = models.IntegerField(default=2)
    golem_attack_phase = models.CharField(max_length=4,
                                        choices=settings.ALLOWED_PHASES, default='4')
    healing_power = models.IntegerField(default=0)
    healing_cost = models.IntegerField(default=2)
    mana_current = models.IntegerField(default=0)
    mana_max = models.IntegerField(default=0)
    health_current = models.IntegerField(default=0)
    health_max = models.IntegerField(default=0)
    hand = models.ManyToManyField(Hand_card)

    def __str__(self):
        return str(self.user)
