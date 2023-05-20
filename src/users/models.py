import uuid

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from safedelete.models import SafeDeleteModel

from crypto.models import CryptoCurrency

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=(
    "Phone number must be entered in the format:'+999999999'.Up to 15 digits"
    " allowed."))


class Account(TimeStampedModel, SafeDeleteModel):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,
                            primary_key=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                related_name="%(class)s_user", null=True)


class AdminAccount(Account):
    pass


class UserAccount(Account):
    phone = models.TextField(validators=[phone_regex])


class UserBalance(TimeStampedModel, SafeDeleteModel):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                             related_name="user_balance")
    currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE,
                                 related_name="user_balance_currency")
    balance = models.DecimalField(max_digits=20, decimal_places=8,
                                  default=0,
                                  validators=[
                                      MinValueValidator(0)
                                  ])
