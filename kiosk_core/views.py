from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from kiosk_core.serializers import CardValidator, CardSerializer
from django.contrib import messages
from django.http import HttpResponseRedirect
from kiosk_core.models import Card


def index(request):
    return render(request, 'kiosk_pages/first_page.html', {})


def show(request):
    return render(request, 'kiosk_pages/show.html',{})

class CardViewset(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def scan(self, request):
        if request.method == 'POST':
            card_data = CardValidator(data=request.data)
            # check if the scaned card doesn't exist or is unvalid
            if not card_data.is_valid():
                messages.add_message(request, messages.WARNING,
                f"Wrong card, please try again")
                return HttpResponseRedirect('/')

            card_number = card_data.validated_data.get('number')

            card_obj = Card.objects.get(number=card_number)
            card_serialized = CardSerializer(Card, many=False)
            card = card_serialized.data
            return render(request,
                'kiosk_pages/show.html',
                {'card':card} )


