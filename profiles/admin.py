from django.contrib import admin
from .models import *
# Register your models here.


class CardAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'in_freeversion',
        'image',
    )

class Player_typeAdmin(admin.ModelAdmin):
    list_display = (
        'selected',
        'image_idle',
    )


admin.site.register(Player)
admin.site.register(Card, CardAdmin)
admin.site.register(Hand_card)
admin.site.register(Player_type,Player_typeAdmin)
admin.site.register(Profile)
