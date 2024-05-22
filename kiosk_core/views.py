from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from kiosk_core.serializers import CardValidator, CardSerializer, AmouuntValidator, BillValidator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from kiosk_core.models import Card, ReededCardFromNfc, PaimentChoice
from django.utils import timezone


# First page and the recharge of the first page if no card has been scanned
def index(request):
    last_scanned = ReededCardFromNfc.objects.all().order_by('created_at').last()
    if last_scanned:
        # Check if the last card has been scaned the last 2 seconds
        if last_scanned.created_at >= timezone.now() - timezone.timedelta(seconds=2):
            return render(request, 'kiosk_pages/send_card.html'
                   ,{'tag_id': last_scanned.reeded_card,
                             })

    return render(request, 'kiosk_pages/first_page.html')



@csrf_exempt
def given_bill(request):
    print('____________________')
    if request.method == 'POST':
        given_bill = request.POST.get('bill')

    print("Given Bill: ", given_bill)

    return HttpResponse(given_bill)



class CardViewset(viewsets.ViewSet):
    # save scanded card:
    @action(detail=False, methods=['POST'])
    def save_scanded_card(self, request):
        scanned_card_id = request.POST.get('scanded_tag_id')
        ReededCardFromNfc.objects.create(reeded_card=scanned_card_id)
        return HttpResponse(scanned_card_id)


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


    # On this part we gather the total of amount selected
    @action(detail=False, methods=['POST'])
    def recharge(self,request):
        selected_data = AmouuntValidator(data=request.data)
        # If it happens that the uuid or the total is wrong
        if not selected_data.is_valid():
            message = "Error, please try again!"

            return render(request, 'kiosk_pages/first_page.html',
                          {'message':message})

        uuid = selected_data.validated_data.get('uuid')
        total = selected_data.validated_data.get('total')

        return render(request,
        'kiosk_pages/recharge.html',
        {'total':total, 'uuid': uuid})


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
        card = Card.objects.get(uuid=uuid)
        paiment_choice = PaimentChoice.objects.create(choice_amount=total,card_uuid=card)
        context = {'uuid': uuid, 'total': total, 'paiment_choice': paiment_choice}
        return render(request, 'paiment/paiement.html', context=context)


    # Amoount of bills recived from the device
    @action(detail=False, methods=['POST'])
    def devices_bill(self,request):
        paiment_choice = PaimentChoice.objects.all().order_by('created_at').last()
        bill_data = BillValidator(data=request.data)
        if not bill_data.is_valid():
            message = ("Sorry error device, please take your bill from the device "
                       "and, restart again please")
            return render(request, 'kiosk_pages/first_page.html'
                          ,{'message':message},)

        amount_device = bill_data.validated_data.get('bill')
        paiment_choice.device_amount += amount_device
        paiment_choice.save()
        return HttpResponse(paiment_choice)


    @action(detail=False, methods=['GET'])
    def return_device(self,request):
        paiment_complete = False
        paiment_choice = PaimentChoice.objects.all().order_by('created_at').last()
        rest = paiment_choice.choice_amount - paiment_choice.device_amount
        if rest <= 0:
            paiment_complete = True
            rest_device = False
            if rest < 0:
                rest_device = True
                rest = paiment_choice.device_amount - paiment_choice.choice_amount
            return render(request,
            'paiment/device_bills.html',
            {'paiment_complete': paiment_complete,
             'rest_device': rest_device, 'rest': rest})
        return render(request,
        'paiment/device_bills.html',
    {'paiment_choice': paiment_choice, 'rest': rest})


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


# This method will recharge paiment page
def recharge_paiment_pg(request):
    uuid = request.POST.get('uuid')
    total = request.POST.get('total')
    choice_amount = request.POST.get('choice_amount')
    devic_amount = request.POST.get('devic_amount')
    context = {'uuid': uuid, 'total': total,
               'choice_amount': choice_amount, 'devic_amount': devic_amount}
    return render(request, 'paiment/recharge_paiment_pg.html',context=context)


# # recharging value
# def recharge(request):
#     if request.method == 'POST':
#         total = request.POST.get('total')
#         uuid = request.POST.get('uuid')
#     return render(request,
#     'kiosk_pages/recharge.html',
#     {'total':total, 'uuid': uuid})


# Stripe ----------------
def stripe_paiment(request):
    return render(request, 'paiment/stripe_paiment.html')


