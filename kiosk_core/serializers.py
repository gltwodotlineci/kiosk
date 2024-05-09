from kiosk_core.models import Card
from rest_framework import serializers

# Validate the number card recived by the miniserver
class CardValidator(serializers.Serializer):

    tag_id = serializers.CharField()
    # check if the given card is right
    def validate_number(self, value):
        try:
            Card.objects.get(number=value)
            return value
        except Card.DoesNotExist:
            raise serializers.ValidationError("The card does not exist")


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

# Serializer to create the data
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


