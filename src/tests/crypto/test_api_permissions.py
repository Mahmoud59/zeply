from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status

from crypto.models import CryptoCurrency
from tests.constants import CRYPTOCURRENCY_NAME_1, CRYPTOCURRENCY_NAME_2


@pytest.mark.django_db
class TestCryptoCurrencyPermission:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.crypto_currency = CryptoCurrency.objects.create(
            name=CRYPTOCURRENCY_NAME_1
        )
        self.url_list = reverse('crypto-currency-list')
        self.url_detail = reverse('crypto-currency-detail',
                                  kwargs={"pk": self.crypto_currency.id})

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_crypto_currency_failed(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = True
        body = {
            'name': CRYPTOCURRENCY_NAME_2
        }
        response = drf_client.post(self.url_list, data=body, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_list_crypto_currencies_failed(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        response = drf_client.get(self.url_list)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_list_crypto_currencies_by_user_failed(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        response = drf_client.get(self.url_list)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_crypto_currency_failed(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_crypto_currency_by_user_failed(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_crypto_currency_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        self.url_detail = reverse('crypto-currency-detail', kwargs={"pk": 55})
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.UserPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_crypto_currency_failed(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        body = {
            "name": CRYPTOCURRENCY_NAME_2
        }
        response = drf_client.patch(self.url_detail, data=body, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_crypto_currency_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        self.url_detail = reverse('crypto-currency-detail', kwargs={"pk": 55})
        body = {
            "name": CRYPTOCURRENCY_NAME_2
        }
        response = drf_client.put(self.url_detail, data=body, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_delete_crypto_currency_failed(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        response = drf_client.delete(self.url_detail)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @patch('utils.permissions.AdminPermission.has_permission')
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_delete_crypto_currency_fail_with_not_exist_id(
            self, mock_authenticate, mock_role, drf_client):
        mock_authenticate.return_value = (MagicMock(), [])
        mock_role.return_value = False
        self.url_detail = reverse('crypto-currency-detail', kwargs={"pk": 55})
        response = drf_client.delete(self.url_detail)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_crypto_currency_no_token_failed(
            self, drf_client):
        body = {
            'name': CRYPTOCURRENCY_NAME_2
        }
        response = drf_client.post(self.url_list, data=body, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
