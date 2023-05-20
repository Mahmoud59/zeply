import uuid as uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from safedelete.models import SafeDeleteModel

from crypto.models import CryptoCurrency
from users.models import UserAccount


class Transaction(TimeStampedModel, SafeDeleteModel):
    class StateType(models.TextChoices):
        PENDING = 'pending', _('pending')
        SUCCESS = 'success', _('success')
        FAILED = 'failed', _('failed')

    uuid = models.UUIDField('User ID', primary_key=True, default=uuid.uuid4)
    currency_amount = models.DecimalField(max_digits=20, decimal_places=8,
                                          default=0,
                                          validators=[
                                              MinValueValidator(0)
                                          ])
    currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE,
                                 related_name="transaction_currency")
    sender_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                    related_name="sender_user")
    receiver_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                      related_name="receiver_user")
    state = models.TextField('State', max_length=7, choices=StateType.choices,
                             default=StateType.PENDING)

    @atomic
    def save(self, **kwargs):
        sender_user = get_object_or_404(UserAccount,
                                        uuid=self.sender_user.uuid)
        receiver_user = get_object_or_404(UserAccount,
                                          uuid=self.receiver_user.uuid)

        if self.created and self.state == 'success':
            if self.currency.name == "BTC":
                sender_currency = sender_user.user_balance.get(currency=self.currency)
                receiver_currency = receiver_user.user_balance.get(currency=self.currency)
                sender_currency.balance -= self.currency_amount
                receiver_currency.balance += self.currency_amount
                sender_currency.save()
                receiver_currency.save()
            elif self.currency.name == "ETH":
                sender_currency = sender_user.user_balance.get(currency=self.currency)
                receiver_currency = receiver_user.user_balance.get(currency=self.currency)
                sender_currency.balance -= self.currency_amount
                receiver_currency.balance += self.currency_amount
                sender_currency.save()
                receiver_currency.save()
        else:
            if sender_user == receiver_user:
                raise ValidationError("Sender can't be receiver in the same "
                                      "transaction.")
            elif sender_user.user_balance.get(
                    currency=self.currency).balance < self.currency_amount:
                raise ValidationError("Sender amount for transactions is less "
                                      "than this transaction amount.")
            elif self.currency.name == "BTC":
                if self.currency_amount > sender_user.user_balance.get(
                        currency=self.currency).balance:
                    raise ValidationError("Sender bitcoin amount not enough.")

            elif self.currency.name == "ETH":
                if self.currency_amount > sender_user.user_balance.get(
                        currency=self.currency).balance:
                    raise ValidationError("Sender ethereum amount not enough.")

        super().save(**kwargs)
