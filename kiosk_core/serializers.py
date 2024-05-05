from kiosk_core.models import Card
from rest_framework import serializers

# Validate the number card recived by the miniserver
class CardValidator(serializers.Serializer):
    number = serializers.CharField()

    # check if the given card is right
    def validate_number(self, value):
        try:
            Card.objects.get(number=value)
            return value
        except Card.DoesNotExist:
            raise serializers.ValidationError("The card does not exist")


# Serializer to create the data
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


