from IPython.utils.coloransi import value
from rest_framework.generics import get_object_or_404

from kiosk_core.models import Card, PaimentChoice
from rest_framework import serializers

# from kiosk_core.views import payement


# Validate the number card recived by the miniserver
class TagIdValidator(serializers.Serializer):
    tag_id = serializers.CharField()

    def validate_tag_id(self, value):
        try:
            get_object_or_404(Card, tag_id=value)
            return value
        except Card.DoesNotExist:
            raise serializers.ValidationError("Card does not exist")


# Validate tag id send by client web socket and send crd
class CardValidator(serializers.Serializer):
    tag_id = serializers.CharField()

    def validate_tag_id(self, value):
        try:
            card =  get_object_or_404(Card, tag_id=value)
            return card
        except Card.DoesNotExist:
            raise serializers.ValidationError("Invalid card send by JS client websocket")


# validate data send from choosing amount
class ChargeValidator(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)
    amount = serializers.IntegerField(required=True)
    tag_id = serializers.CharField()

    def validate_uuid(self, value):
        try:
            get_object_or_404(Card, uuid=value)
            return value
        except Card.DoesNotExist:
            raise serializers.ValidationError("Invalid card from amount choice")

    # validate that number given as a string is a number
    def validate_amount(self, value):
        if value.is_integer():
            return value

        raise serializers.ValidationError("The amount must be an integer")

    def validate_tag_id(self, value):
        try:
            get_object_or_404(Card, tag_id=value)
            return value
        except Card.DoesNotExist:
            raise serializers.ValidationError("Card does not exist")

# Validating choosed amount and card uuid
class AmouuntValidator(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)
    payement_choice_id = serializers.UUIDField()
    amount = serializers.CharField(required=True)
    type_payement = serializers.CharField()
    device_confirm_paiment = serializers.CharField(required=False)

    def validate_uuid(self, value):
        try:
            Card.objects.get(uuid=value)
            return value
        except Card.DoesNotExist:
            raise serializers.ValidationError("Card error")

    def validate_amount(self, value):
        if value.isdigit():
            return value
        raise serializers.ValidationError("The amount must be an string")

    def validate_type_payement(self, value):
        if value in ['cash', 'cb']:
            return value
        raise serializers.ValidationError("Invalid  choice")

    # validating if the payement choice obj exist
    def validate_payement_choice_id(self, value):
        try:
            PaimentChoice.objects.filter(pk=value).exists()
            return value
        except PaimentChoice.DoesNotExist:
            raise serializers.ValidationError("Invalid id for payement choice")


# Validate bill amount given from websocket server
class BillValidator(serializers.Serializer):
    bill = serializers.IntegerField(required=True)
    payement_choice_id = serializers.UUIDField()
    amount = serializers.IntegerField()
    uuid = serializers.UUIDField(required=True)

    def validate_bill(self, value):
        if value in [5,10, 20, 50, 100]:
            return value

        raise serializers.ValidationError("Invalid  bill amount given")

    def validate_amount(self, value):
        return value

    def validate_uuid(self, value):
        return value


    # validating if the payement choice obj exist
    def validate_payement_choice_id(self, value):
        try:
            PaimentChoice.objects.filter(pk=value).exists()
            return value
        except PaimentChoice.DoesNotExist:
            raise serializers.ValidationError("Invalid id for payment choice")
