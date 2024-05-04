from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')

# Creating a card model
class Card(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid)
    number = models.CharField(max_length=3, unique=True, verbose_name='Number')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='amount')
