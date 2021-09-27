from django.db import models
from django.conf import settings
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
    allowed_in_phase = models.CharField(max_length=4, choices=settings.ALLOWED_PHASES)
    attack_all = models.BooleanField(default=False)
    skill_style = models.CharField(max_length=2, choices=settings.SKILL_STYLES)
    mana_cost = models.IntegerField(default=2)
    cards_discard_cost = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Player(models.Model):

    date_time_created = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Player_type, on_delete=models.CASCADE)
    fire_defense = models.IntegerField(default=0)
    ice_defense = models.IntegerField(default=0)
    drain_defense = models.IntegerField(default=0)
    thunder_defense = models.IntegerField(default=0)
    physical_defense = models.IntegerField(default=0)
    fire_attack_power = models.IntegerField(default=0)
    fire_attack_cost = models.IntegerField(default=0)
    ice_attack_power = models.IntegerField(default=0)
    ice_attack_cost = models.IntegerField(default=0)
    drain_attack_power = models.IntegerField(default=0)
    drain_attack_cost = models.IntegerField(default=0)
    thunder_attack_power = models.IntegerField(default=0)
    thunder_attack_cost = models.IntegerField(default=0)
    golem_attack_power = models.IntegerField(default=0)
    golem_attack_cost = models.IntegerField(default=0)
    healing_power = models.IntegerField(default=0)
    healing_attack_cost = models.IntegerField(default=0)
    mana_current = models.IntegerField(default=0)
    mana_max = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    health_current = models.IntegerField(default=0)
    health_max = models.IntegerField(default=0)
    hand = models.ManyToManyField(Card)

    def __str__(self):
        return str(self.id)
