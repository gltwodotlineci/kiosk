from django.urls import path, include
from kiosk_core.views import index, show, CardViewset, recharge, stripe_paiment
from rest_framework import routers
router = routers.DefaultRouter()

router.register(r'card', CardViewset, basename='scan')

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
    path('recharge/', recharge, name='recharge'),
    path('show/', show, name='show'),
    path('stripe_paiment/', stripe_paiment, name='stripe_paiment'),
]
