import pytest
from django.core.exceptions import ObjectDoesNotExist

from crypto.models import CryptoCurrency
from tests.constants import CRYPTOCURRENCY_NAME_1, CRYPTOCURRENCY_NAME_2


@pytest.mark.django_db
class TestCryptoCurrencyModel:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.crypto_currency = CryptoCurrency.objects.create(
            name=CRYPTOCURRENCY_NAME_1
        )

    def test_get_crypto_currency_objects_success(self):
        assert CryptoCurrency.objects.all().count() == 1

    def test_create_crypto_currency_object_success(self):
        CryptoCurrency.objects.create(
            name=CRYPTOCURRENCY_NAME_2,
        )
        assert CryptoCurrency.objects.all().count() == 2

    def test_get_crypto_currency_object_success(self):
        assert len(CryptoCurrency.objects.filter(id=self.crypto_currency.pk)) == 1

    def test_get_crypto_currency_object_fail_with_not_exist_id(self):
        with pytest.raises(ObjectDoesNotExist):
            CryptoCurrency.objects.get(id=55)
