from django.contrib import admin
from .models import Player
from .models import Card
from .models import HandCard
from .models import Profile
from .models import PlayerType
# Register your models here.


class CardAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'in_freeversion',
        'image',
    )

class PlayerTypeAdmin(admin.ModelAdmin):
    list_display = (
        'selected',
        'image_idle',
    )


admin.site.register(Player)
admin.site.register(Card, CardAdmin)
admin.site.register(HandCard)
admin.site.register(PlayerType,PlayerTypeAdmin)
admin.site.register(Profile)
