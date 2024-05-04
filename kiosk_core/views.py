from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action


def index(request):
    return render(request, 'kiosk_pages/first_page.html', {})


def show(request):
    return render(request, 'kiosk_pages/show.html',{})

class CardViewset(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def scan(self, request):
        pass


