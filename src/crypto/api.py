from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from crypto.helpers import AddressGenerator
from crypto.models import Address, CryptoCurrency
from crypto.serializers import AddressSerializer, CryptoCurrencySerializer
from utils.permissions import AdminPermission, UserPermission


class CryptoCurrencyViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, AdminPermission)
    serializer_class = CryptoCurrencySerializer
    queryset = CryptoCurrency.objects.order_by('-id')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = (IsAuthenticated, AdminPermission
                                       | UserPermission)
        return super().get_permissions()


class CryptoAddressViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, UserPermission)
    serializer_class = AddressSerializer
    queryset = Address.objects.order_by('-id')

    def create(self, request, *args, **kwargs):
        requested_currency = get_object_or_404(
            CryptoCurrency, name=request.data.get('currency', None))
        private_key, request.data['address'] = \
            AddressGenerator().generate_address(requested_currency.name)
        request.data['currency'] = requested_currency.id
        address = super().create(request, *args, **kwargs)
        address.data['private_key'] = private_key
        return Response(address.data, status=status.HTTP_201_CREATED)
