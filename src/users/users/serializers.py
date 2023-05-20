from rest_framework import serializers

from users.models import UserAccount
from users.serializers import ListUserSerializer, UserBalanceSerializer


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        exclude = ('uuid',)


class ListUserModelSerializer(serializers.ModelSerializer):
    user = ListUserSerializer()
    user_balance = UserBalanceSerializer(many=True)

    class Meta:
        model = UserAccount
        fields = '__all__'
