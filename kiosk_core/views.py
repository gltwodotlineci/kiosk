from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from kiosk_core.serializers import CardValidator, CardSerializer, AmouuntValidator
from django.contrib import messages
from django.http import HttpResponseRedirect
from kiosk_core.models import Card
from django.http import HttpResponse


# First page
def index(request):
    return render(request, 'kiosk_pages/first_page.html',
            {})


# Page of interaction of card user and filling values
def show(request):
    return render(request, 'kiosk_pages/show.html',{})


#search the card number with json from the pi server (flask)
def reciving_card_number(request):
    pass



class CardViewset(viewsets.ViewSet):
    # post from card scan /
    @action(detail=False, methods=['POST'])
    def scan(self, request):
        card_data = CardValidator(data=request.data)
        # check if the scaned card doesn't exist or is unvalid
        if not card_data.is_valid():
            message = "Card error, please try again!"

            return render(request, 'kiosk_pages/first_page.html',
                          {'message':message})

        card_number = card_data.validated_data.get('tag_id')
        card_obj = Card.objects.get(tag_id=card_number)
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
        return render(request, 'paiment/paiement.html', context=context)


    @action(detail=False, methods=['POST'])
    def confirmation_paiment(self, request):
        confirmation_data = AmouuntValidator(data=request.data)
        # check if the datas are well selected
        if not confirmation_data.is_valid():
            message = ("Error, of payment, please take the money from the device"
                       "and try again!")

            return render(request, 'paiment/error_paiment.html',
                          {'message':message})

        uuid = confirmation_data.validated_data.get('uuid')
        total = confirmation_data.validated_data.get('total')
        device_confirm_paiment = confirmation_data.validated_data.get('device_confirm_paiment')
        if device_confirm_paiment != None:
            card = Card.objects.get(uuid=uuid)
            card.amount += int(total)
            card.save()
            return render(request, 'paiment/confirmation_paiement.html',{'card': card})

        message = ("Error, of payment, please take the money from the device"
                       "and try again!")

        return render(request, 'paiment/error_paiment.html',
                          {'message':message})



# recharging value
def recharge(request):
    if request.method == 'GET':
        total = request.GET.get('total')
        uuid = request.GET.get('uuid')
    return render(request,
    'kiosk_pages/recharge.html',
    {'total':total, 'uuid': uuid})


# Stripe ----------------
def stripe_paiment(request):
    return render(request, 'paiment/stripe_paiment.html')
