from django.db.models.signals import post_save
from django.dispatch import receiver

from crypto.models import CryptoCurrency
from users.models import UserAccount
from users.serializers import UserBalanceSerializer


@receiver(post_save, sender=UserAccount)
def post_save_user_account(sender, instance, created, **kwargs):
    print(created)
    if created:
        print(222222222222222222222222222)
        for currency in CryptoCurrency.objects.all():
            print(currency)
            user_balance = UserBalanceSerializer(data={
                'user': instance.pk,
                'currency': currency.pk
            })
            user_balance.is_valid(raise_exception=True)
            user_balance.save()
