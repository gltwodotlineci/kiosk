from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from kiosk_core.serializers import CardValidator, CardSerializer, AmouuntValidator
from django.contrib import messages
from django.http import HttpResponseRedirect
from kiosk_core.models import Card


def index(request):
    five = 5
    return render(request, 'kiosk_pages/first_page.html', {'five':five})


def show(request):
    return render(request, 'kiosk_pages/show.html',{})

class CardViewset(viewsets.ViewSet):
    # post from card scan /
    @action(detail=False, methods=['POST'])
    def scan(self, request):
        card_data = CardValidator(data=request.data)
        # check if the scaned card doesn't exist or is unvalid
        if not card_data.is_valid():
            messages.add_message(request, messages.WARNING,
                                 f"Wrong card, please try again")
            return HttpResponseRedirect('/')

        card_number = card_data.validated_data.get('number')

        card_obj = Card.objects.get(number=card_number)
        card_serialized = CardSerializer(card_obj, many=False)
        card = card_serialized.data
        return render(request,
                      'kiosk_pages/show.html',
                      {'card': card})


    # post from paiment
    @action(detail=False, methods=['POST'])
    def paiment(self, request):
        choosed_data = AmouuntValidator(data=request.data)
        # check if the datas are well selected
        if not choosed_data.is_valid():
            messages.add_message(request, messages.WARNING,
            "Wrong selection, please try again")
            return HttpResponseRedirect('/')
        uuid = choosed_data.validated_data.get('uuid')
        total = choosed_data.validated_data.get('total')
        context = {'uuid': uuid, 'total': total}
        return render(request, 'kiosk_pages/paiement.html',context=context)


# recharging value
def recharge(request):
    if request.method == 'GET':
        total = request.GET.get('total')
        uuid = request.GET.get('uuid')
    return render(request,
    'kiosk_pages/recharge.html',
    {'total':total, 'uuid': uuid})
