import secrets
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')


class DeviceTokenAuthentication(models.Model):
    key = models.CharField(max_length=64, unique=True, default=secrets.token_hex)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    device_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.device_name or 'Unnamed'} ({self.key})"

# Creating a card model
class Card(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tag_id = models.CharField(max_length=50, unique=True, verbose_name='tag id')
    amount = models.IntegerField(default=0, verbose_name='amount')
    qr_nb = models.CharField(max_length=50, unique=True, verbose_name='Qr code number')


# Model that will save each card reeded by the NFC reeder
class ReededCardFromNfc(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reeded_card = models.CharField(max_length=50, unique=False, verbose_name='reeded card')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')


class PaimentChoice(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    card_uuid = models.ForeignKey(Card, on_delete=models.PROTECT, related_name='paiment_choice',verbose_name='card uuid')
    choice_amount = models.IntegerField(verbose_name='choice amount')
    device_amount = models.IntegerField(default=0, verbose_name='device amount', null=True, blank=True)
    rest = models.IntegerField(default=0, verbose_name='rest', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    # method that will calculate the difference between amount choice and device
    def calcule_amount_diff(self):
        if self.device_amount > self.choice_amount:
            self.rest = self.device_amount - self.choice_amount
            self.save()
        return self.choice_amount - self.device_amount

