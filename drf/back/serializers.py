from rest_framework import serializers

from .models import *


class UserItemsSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', max_length=200)
    can_upgrade = serializers.BooleanField(source='product.can_upgrade')

    class Meta:
        model = UserItems
        fields = ['count', 'active', 'product', 'can_upgrade']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistic
        fields = '__all__'        

class UserSerializer(serializers.ModelSerializer):
    product = UserItemsSerializer(many=True, read_only=True)
    profile = UserProfileSerializer(many=True, read_only=True)
    statistic = UserStatisticSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['steamID', 'product', 'profile', 'statistic','coins', 'rp', 'total_coins', 'ban_status', 'add_hero']


class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistory
        fields = ('game_time', 'game_difficulty')