from django.urls import path, include
from kiosk_core.views import index

urlpatterns = [
    path('', index, name='index'),
]
