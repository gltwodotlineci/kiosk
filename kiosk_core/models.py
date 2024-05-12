from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')

# Creating a card model
class Card(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tag_id = models.CharField(max_length=50, unique=True, verbose_name='tag id')
    amount = models.IntegerField(default=0, verbose_name='amount')


# Model that will save each card reeded by the NFC reeder
class ReededCardFromNfc(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reeded_card = models.CharField(max_length=50, unique=False, verbose_name='reeded card')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
