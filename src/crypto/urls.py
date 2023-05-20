from rest_framework.routers import DefaultRouter

from crypto.api import CryptoAddressViewSet, CryptoCurrencyViewSet

router = DefaultRouter()
router.register(r'crypto-currencies', CryptoCurrencyViewSet, basename='crypto-currency')
router.register(r'crypto-addresses', CryptoAddressViewSet, basename='crypto-address')
urlpatterns = router.urls
