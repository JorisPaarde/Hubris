from django.db import models

# Create your models here.


# choices used in various models
ATTACK_PHASES = (
    ('1', 'I'),
    ('2', 'II'),
    ('3', 'III'),
    ('4', 'IV'),
    ('5', 'V'),
)

SKILL_STYLES = (
    ('LN', 'Lightning'),
    ('FR', 'Fire'),
    ('GL', 'Golem'),
    ('DR', 'Drain'),
    ('IC', 'Ice'),
)


class Enemy(models.Model):

    in_fullversion = models.BooleanField(default=True)
    name = models.CharField(max_length=254)
    image_idle = models.ImageField
    image_attack = models.ImageField
    image_die = models.ImageField
    max_health = models.IntegerField
    attack_power = models.IntegerField
    skill_style = models.CharField(max_length=2, choices=SKILL_STYLES)
    attack_phase = models.CharField(max_length=1, choices=ATTACK_PHASES)
    xp_value = models.IntegerField

    def __str__(self):
        return self.name


class Player_type(models.Model):

    PLAYER_STYLES = (
        ('LN', 'Lightning'),
        ('FR', 'Fire'),
        ('IC', 'Ice'),
    )

    selected = models.CharField(max_length=2, choices=PLAYER_STYLES)
    image_idle = models.ImageField
    image_attack = models.ImageField
    image_die = models.ImageField

    def __str__(self):
        return self.selected


class Player_stat(models.Model):

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

    def __str__(self):
        return self


class Card(models.Model):

    ALLOWED_PHASES = (
        ('1', 'I'),
        ('2', 'II'),
        ('3', 'III'),
        ('4', 'IV'),
        ('5', 'V'),
        ('ALL', 'I-V'),
        ('NONE', ''),
    )

    in_fullversion = models.BooleanField(default=True)
    title = models.CharField
    description = models.TextField
    image = models.ImageField
    effect_text = models.CharField
    allowed_in_phase = models.CharField(max_length=4, choices=ALLOWED_PHASES)
    attack_all = models.BooleanField(default=False)
    skill_style = models.CharField(max_length=2, choices=SKILL_STYLES)
    mana_cost = models.IntegerField
    cards_discard_cost = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Hand_card(models.Model):

    date_time_created = models.DateTimeField
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self


class Player(models.Model):

    date_time_created = models.DateTimeField
    type = models.ForeignKey(Player_type, on_delete=models.CASCADE)
    stats = models.ForeignKey(Player_stat, on_delete=models.CASCADE)
    hand = models.ForeignKey(Hand_card, on_delete=models.CASCADE)

    def __str__(self):
        return self


class Game(models.Model):

    GAME_STEPS = (
        ('1', 'Step 1'),
        ('2', 'Step 2'),
        ('3', 'Step 3'),
        ('4', 'Step 4'),
        ('5', 'Step 5'),
    )

    date_time_created = models.DateTimeField
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.BigIntegerField(default=0)
    game_step = models.CharField(max_length=1, choices=GAME_STEPS)

    def __str__(self):
        return self


class Current_game_floor(models.Model):

    date_time_created = models.DateTimeField
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    current_phase = models.CharField(max_length=1, choices=ATTACK_PHASES)

    def __str__(self):
        return self


class Game_floor_enemy(models.Model):

    health_current = models.IntegerField
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)
    game_floor = models.ForeignKey(Current_game_floor,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self
