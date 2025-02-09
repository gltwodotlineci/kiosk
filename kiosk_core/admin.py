from django.contrib import admin
from kiosk_core.models import Card

# Creating admin for card nb
class CardAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'qr_nb')

admin.site.register(Card, CardAdmin)
