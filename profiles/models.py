"""
Profile app models
-------------------------
Classes for Profile app:
    - PlayerType
    - Card
    - HandCard
    - Player
    - Profile
"""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.

class BaseClass(models.Model):
    """
    Model to keep classes ordered by primary key in the database.
    """
    class Meta:
        """
        order by primary key.
        """
        ordering = ['pk']
        abstract = True


class PlayerType(BaseClass):
    """
    Model for Player types.
    -Selected type.
    -Images.
    """
    selected = models.CharField(max_length=2, choices=settings.PLAYER_STYLES)
    image_idle = models.ImageField(null=True, blank=True)
    image_attack = models.ImageField(null=True, blank=True)
    image_die = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.selected)


class Card(BaseClass):
    """
    Model for creating cards.
    -Indication of availability in free version.
    -Title.
    -Description.
    -Image.
    -Effect text.
    -Allowed in phase.
    -Skill style.
    -Allowed in phase.
    -Stats.
    """
    in_freeversion = models.BooleanField(default=True)
    title = models.CharField(max_length=254, blank=True)
    description = models.TextField(max_length=1024, blank=True)
    image = models.ImageField(null=True, blank=True)
    effect_text = models.CharField(max_length=254, blank=True)
    allowed_in_phase = models.CharField(max_length=4,
                                        choices=settings.ALLOWED_PHASES)
    attack_all = models.BooleanField(default=False)
    skill_style = models.CharField(max_length=2, choices=settings.SKILL_STYLES)
    attack_modifier = models.IntegerField(default=0)
    healing_modifier = models.IntegerField(default=0)
    health_modifier = models.IntegerField(default=0)
    mana_modifier = models.IntegerField(default=0)
    defence_modifier = models.IntegerField(default=0)
    mana_cost = models.IntegerField(default=2)
    cards_discard_cost = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)


class HandCard(BaseClass):
    """
    Model for creating Handcards.
    A set of 8 of these are created for each player.
    -Associated card.
    """

    date_time_created = models.DateTimeField(auto_now=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.card)


class Player(BaseClass):
    """
    Model for creating players.
    These are created for each user.
    -Associated user.
    -Associated playertype.
    -Player stats.
    -Hand with associated handcards.
    """
    date_time_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(PlayerType, on_delete=models.CASCADE, null=True)
    fire_attack_power = models.IntegerField(default=0)
    fire_defense = models.IntegerField(default=0)
    fire_attack_cost = models.IntegerField(default=3)
    fire_attack_phase = models.CharField(max_length=4,
                                         choices=settings.ALLOWED_PHASES,
                                         default='2')
    ice_attack_power = models.IntegerField(default=0)
    ice_defense = models.IntegerField(default=0)
    ice_attack_cost = models.IntegerField(default=2)
    ice_attack_phase = models.CharField(max_length=4,
                                        choices=settings.ALLOWED_PHASES,
                                        default='3')
    drain_attack_power = models.IntegerField(default=0)
    drain_defense = models.IntegerField(default=0)
    drain_attack_cost = models.IntegerField(default=1)
    drain_attack_phase = models.CharField(max_length=4,
                                          choices=settings.ALLOWED_PHASES,
                                          default='ALL')
    lightning_attack_power = models.IntegerField(default=0)
    lightning_defense = models.IntegerField(default=0)
    lightning_attack_cost = models.IntegerField(default=2)
    lightning_attack_phase = models.CharField(max_length=4,
                                              choices=settings.ALLOWED_PHASES,
                                              default='1')
    golem_attack_power = models.IntegerField(default=0)
    physical_defense = models.IntegerField(default=0)
    golem_attack_cost = models.IntegerField(default=2)
    golem_attack_phase = models.CharField(max_length=4,
                                          choices=settings.ALLOWED_PHASES,
                                          default='4')
    healing_power = models.IntegerField(default=0)
    healing_cost = models.IntegerField(default=2)
    mana_current = models.IntegerField(default=0)
    mana_max = models.IntegerField(default=0)
    health_current = models.IntegerField(default=0)
    health_max = models.IntegerField(default=0)
    hand = models.ManyToManyField(HandCard)

    def __str__(self):
        return str(self.user)

# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone


class Profile(BaseClass):
    """
    Model to extend user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    payed_full_version = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """create a profile when  a user is created"""
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        """save a profile when a user is saved"""
        instance.profile.save()

    def __str__(self):
        return str(self.user)
