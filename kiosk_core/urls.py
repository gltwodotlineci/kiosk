from django.urls import path, include
from kiosk_core.views import index, show

urlpatterns = [
    path('', index, name='index'),
    path('show/', show, name='show')
]
