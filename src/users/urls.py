from django.urls import path
from rest_framework.routers import DefaultRouter

from users.admins.api import AdminViewSet
from users.api import UserLoginAPIView
from users.users.api import UserViewSet

urlpatterns = [
    # Login
    path('users/login/', UserLoginAPIView.as_view(),
         name='users-login'),

    # Admin
    path('admins/', AdminViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='admin-list'),
    path('admins/<str:uuid>/', AdminViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='admin-detail'),

    # User
    path('users/', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='user-list'),
    path('users/<str:uuid>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user-detail'),
]

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns += router.urls
