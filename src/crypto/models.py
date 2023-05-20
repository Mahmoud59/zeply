from django.db import models
from django_extensions.db.models import TimeStampedModel
from safedelete.models import SafeDeleteModel


class CryptoCurrency(TimeStampedModel, SafeDeleteModel):
    name = models.CharField('Name', max_length=50, unique=True)


class Address(TimeStampedModel, SafeDeleteModel):
    currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, unique=True)
