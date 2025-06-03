from django.contrib import admin
from kiosk_core.models import Card, DeviceTokenAuthentication

# Creating admin for card nb
class CardAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'qr_nb')


class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ("key", "device_name", "created_at")


admin.site.register(DeviceTokenAuthentication, DeviceTokenAdmin)
admin.site.register(Card, CardAdmin)
