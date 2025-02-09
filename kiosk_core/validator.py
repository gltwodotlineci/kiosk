from rest_framework.generics import get_object_or_404

from kiosk_core.models import Card
from rest_framework import serializers

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
    uuid = serializers.UUIDField(read_only=True)
    amount = serializers.IntegerField()

    def validate_uuid(self, value):
        try:
            get_object_or_404(Card, uuid=value)
            print("V____V ", value)
            return value
        except Card.DoesNotExist:
            raise serializers.ValidationError("Invalid card from amount choice")


    # validate that number given as a string is a number
    def validate_amount(self, value):
        if value.is_integer():
            return value
        else:
            raise serializers.ValidationError("The amount must be an integer")
