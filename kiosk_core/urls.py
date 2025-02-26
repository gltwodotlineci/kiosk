from django.urls import path, include
from kiosk_core.views import (CardViewset, home, error_scan, #given_bill, recharge_paiment_pg
                              stripe_paiment, scan_page)
from rest_framework import routers
router = routers.DefaultRouter()

router.register(r'card', CardViewset, basename='scan')


urlpatterns = [
    path('', home, name='home'),
    path('scanpage', scan_page, name='index'),

    path('error_scan', error_scan, name='error_scan'),
    path('api/', include(router.urls)),
    # path('recharge_paiment_pg/', recharge_paiment_pg, name='recharge_paiment_pg'),
    # path('given_bill/', given_bill, name='given_bill'),
    # path('recharge/', recharge, name='recharge'),
    path('stripe_paiment/', stripe_paiment, name='stripe_paiment'),
]
