from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status

from crypto.models import Address, CryptoCurrency
from tests.constants import (
    CRYPTOADDRESS_NAME_1, CRYPTOADDRESS_NAME_2, CRYPTOCURRENCY_NAME_1,
    CRYPTOCURRENCY_NAME_2,
)


class TestCryptoCurrencyEndpoints:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.crypto_currency = CryptoCurrency.objects.create(
            name=CRYPTOCURRENCY_NAME_1
        )
        self.url_list = reverse('crypto-currency-list')
        self.url_detail = reverse('crypto-currency-detail',
                                  kwargs={"pk": self.crypto_currency.id})

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_crypto_currency_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        body = {
            'name': CRYPTOCURRENCY_NAME_2
        }
        response = drf_client.post(self.url_list, data=body, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert CryptoCurrency.objects.all().count() == 2

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_list_crypto_currencies_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        response = drf_client.get(self.url_list)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_list_crypto_currencies_by_user_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        response = drf_client.get(self.url_list)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_crypto_currency_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_200_OK

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_crypto_currency__by_user_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_200_OK

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_crypto_currency_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        self.url_detail = reverse('crypto-currency-detail', kwargs={"pk": 55})
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_crypto_currency_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        body = {
            "name": CRYPTOCURRENCY_NAME_2
        }
        response = drf_client.patch(self.url_detail, data=body, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == self.crypto_currency.id

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_crypto_currency_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        self.url_detail = reverse('crypto-currency-detail', kwargs={"pk": 55})
        body = {
            "name": CRYPTOCURRENCY_NAME_2
        }
        response = drf_client.put(self.url_detail, data=body, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_delete_crypto_currency_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        response = drf_client.delete(self.url_detail)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_delete_crypto_currency_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        self.url_detail = reverse('crypto-currency-detail', kwargs={"pk": 55})
        response = drf_client.delete(self.url_detail)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCryptoAddressEndpoints:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.crypto_currency = CryptoCurrency.objects.create(
            name=CRYPTOCURRENCY_NAME_1
        )
        self.crypto_address = Address.objects.create(
            address=CRYPTOADDRESS_NAME_1,
            currency=self.crypto_currency
        )
        self.url_list = reverse('crypto-address-list')
        self.url_detail = reverse('crypto-address-detail',
                                  kwargs={"pk": self.crypto_address.id})

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_crypto_address_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        body = {
            'currency': CRYPTOCURRENCY_NAME_1
        }
        response = drf_client.post(self.url_list, data=body, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Address.objects.all().count() == 2

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_list_crypto_addresses_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        response = drf_client.get(self.url_list)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_crypto_address_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_200_OK

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_crypto_address_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        self.url_detail = reverse('crypto-address-detail', kwargs={"pk": 55})
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_crypto_address_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        body = {
            "address": CRYPTOADDRESS_NAME_2
        }
        response = drf_client.patch(self.url_detail, data=body, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == self.crypto_address.id

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_crypto_address_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        self.url_detail = reverse('crypto-address-detail', kwargs={"pk": 55})
        body = {
            "name": CRYPTOADDRESS_NAME_2
        }
        response = drf_client.put(self.url_detail, data=body, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_delete_crypto_address_success(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        response = drf_client.delete(self.url_detail)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_delete_crypto_address_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        self.url_detail = reverse('crypto-address-detail', kwargs={"pk": 55})
        response = drf_client.delete(self.url_detail)
        assert response.status_code == status.HTTP_404_NOT_FOUND
