import json
from crypt import methods
from http.client import responses
from pickle import FALSE

from django.shortcuts import render
from django.template.loader import render_to_string
from django_browser_reload.views import message
from rest_framework import viewsets
from rest_framework.decorators import action
from kiosk_core.serializers import BillValidator
from kiosk_core.validator import (TagIdValidator, CardValidator, ChargeValidator,
        AmouuntValidator, BillValidator)
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from kiosk_core.models import Card, ReededCardFromNfc, PaimentChoice
from django.http import JsonResponse
import os
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt


def home(request):

    return  render(request, 'kiosk_pages/home.html')


# First page and the recharge of the first page if no card has been scanned
def scan_page(request):
    context  = {'ip_nav_deported':os.environ.get('IP_NAV_DEPORTED'),
                'used_ip_deported': os.environ.get('USED_IP_NAV_DEPORTED')
                }
    return render(request, 'kiosk_pages/scan_page.html', context)


# If wrong card scaned
def error_scan(request):
    render_template = render_to_string(
            'kiosk_pages/card_error.html'
    )
    return JsonResponse({'html': render_template, 'error': 'yes'})


class CardViewset(viewsets.ViewSet):

    # post from card scan
    @action(detail=False, methods=['POST'])
    def scan(self, request):
        tag_id_validator = TagIdValidator(data=request.data)
        response = {'message': "Failed", 'tag_id': ''}
        # check if the scaned card doesn't exist or is unvalid
        if not tag_id_validator.is_valid():
            return HttpResponse(json.dumps(response))

        # send the tag_id if the card exists
        tag_id = tag_id_validator.validated_data.get('tag_id')
        response['message'] = "Found"
        response['tag_id'] = tag_id
        return HttpResponse(json.dumps(response))

    # sending to charging card page
    @action(detail=False, methods=['POST'])
    def charg_card(self, request):
        card_validator = CardValidator(data=request.data)
        if not card_validator.is_valid():
            pass
        card = card_validator.validated_data.get('tag_id')

        render_template = render_to_string(
            'kiosk_pages/show_amount.html', {'card': card}
        )
        return JsonResponse({'html': render_template})



    # On this part we gather the total of amount selected
    @action(detail=False, methods=['POST'])
    def recharge(self,request):
        selected_data = ChargeValidator(data=request.data)
        # If it happens that the uuid or the total is wrong
        if not selected_data.is_valid():
            message = "Error, please try again!"
            print("NOt VAlidddddd: ", selected_data)
            return render(request, 'kiosk_pages/first_page.html/',
                          {'message':message})

        uuid = selected_data.validated_data.get('uuid')
        amount = selected_data.validated_data.get('amount')
        tag_id = selected_data.validated_data.get('tag_id')
        card = Card.objects.get(uuid=uuid)
        payement_choice = PaimentChoice(card_uuid = card, choice_amount = amount)
        payement_choice.save()
        payement_choice_id = payement_choice.pk

        return render(request,
                      'payement/choose_payement.html/',
                      {'amount':amount,
                               'uuid': uuid,
                               'tag_id': tag_id,
                               'payement_choice_id': payement_choice_id
                            })


    # post from payement
    @action(detail=False, methods=['POST'])
    def payement(self, request):
        # Validating the data from choosed amount
        choosed_data = AmouuntValidator(data=request.data)
        # check if the datas are well selected
        if not choosed_data.is_valid():
            messages.add_message(request, messages.WARNING,
            "Wrong selection, please try again")
            return HttpResponseRedirect('/')
        uuid = choosed_data.validated_data.get('uuid')
        amount = choosed_data.validated_data.get('amount')
        type_payement = choosed_data.validated_data.get('type_payement')
        payement_choice_id = choosed_data.validated_data.get('payement_choice_id')

        context = {'uuid': uuid,
                   'amount': amount,
                   #'paiement_choice': type_payement,
                   'payement_choice_id': payement_choice_id
                   }

        # Send to cash payement page
        if type_payement == "cash":
            return render(request, 'payement/payement.html', context=context)

        # Send to CB payement page
        return render(request, 'payement/payement_cb.html', context=context)


    # Amoount of bills recived from the device
    @action(detail=False, methods=['POST'])
    def devices_bill(self,request):
        # parse the json data from JS fetch
        data = json.loads(request.body)
        # Validating bill data
        data_bill =  BillValidator(data=data)
        if not data_bill.is_valid():
            print("NOt valid bill")
            return HttpResponseRedirect('/')

        # Reciving the data
        bill = data_bill.validated_data.get('bill')
        uuid = data_bill.validated_data.get('uuid')
        amount = data_bill.validated_data.get('amount')
        choosed_payement = data_bill.validated_data.get('payement_choice_id')

        payement_choice = PaimentChoice.objects.get(uuid=choosed_payement)
        payement_choice.device_amount += bill

        payement_choice.rest = payement_choice.device_amount - payement_choice.choice_amount
        card = Card.objects.get(uuid=uuid)

        payement_choice.save()
        data = None

        # New page with the confirmation of charging!
        if payement_choice.rest >= 0:
            card.amount += payement_choice.choice_amount
            card.save()
            # return confirmation page to JS fetch
            render_template = render_to_string('payement/confirmation_paiement.html',
                          {'amount': card.amount,
                                'rest': payement_choice.rest,
                                'complete': 'yes'}
                          )
            return JsonResponse({'html': render_template, 'complete': 'yes'})

        # return the same page to JS fetch, but with new data
        # The choosed sum is not completed jet
        render_same_template = render_to_string('payement/payement.html',
                                {'uuid': card.pk,
                                'amount': amount,
                                 'payement_choice_id': payement_choice.pk,
                                 'given_bill': payement_choice.device_amount
                                 })
        return JsonResponse({'html': render_same_template, 'complete': 'no'})


# Stripe ----------------
def stripe_paiment(request):
    return render(request, 'payement/stripe_paiment.html')
