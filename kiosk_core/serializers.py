from kiosk_core.models import Card
from rest_framework import serializers

# Validate the amount and uuid posted
class AmouuntValidator(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)
    total = serializers.CharField(required=True)
    device_confirm_paiment = serializers.CharField(required=False)

    def validate_uuid(self, value):
        try:
            Card.objects.get(uuid=value)
            return value
        except Card.DoesNotExist:
            raise serializers.ValidationError("Card error")


class BillValidator(serializers.Serializer):
    bill = serializers.IntegerField()

    def validate_bill(self, value):
        try:
            value in [5,10,20,50]
            return value
        except ValueError: # We have to check how to send the error to
            # the device ...
            raise serializers.ValidationError("Bill error")


