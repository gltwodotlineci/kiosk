from django.urls import path, include
from kiosk_core.views import (index, CardViewset, recharge, index_bis,
                stripe_paiment, saving_scanned_card)
from rest_framework import routers
router = routers.DefaultRouter()

router.register(r'card', CardViewset, basename='scan')

urlpatterns = [
    path('', index, name='index'),
    path('index_bis/', index_bis, name='index_bis'),
    path('scaned_id/', saving_scanned_card, name='scaned_id'),
    path('api/', include(router.urls)),
    path('recharge/', recharge, name='recharge'),
    path('stripe_paiment/', stripe_paiment, name='stripe_paiment'),
]

    #path('recharge_paiment_pg/', recharge_paiment_pg, name='recharge_paiment_pg'),
