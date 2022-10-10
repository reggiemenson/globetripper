from rest_framework import serializers
from users.models import User
# from users.serializers import UserSerializer
from .models import Town, Trip, Badge, Group


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'score', 'image', 'towns', 'badges', 'groups_owned', 'groups_requested', 'groups_joined', 'groups_podium1', 'groups_podium2', 'groups_podium3')


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'name', 'start_date', 'end_date', 'user')

class PopulatedTripSerializer(TripSerializer):
    user = UserSerializer()

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'description', 'image', 'users')

class PopulatedBadgeSerializer(BadgeSerializer):
    users = UserSerializer(many=True)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'image', 'owner', 'members', 'requests')
        extra_kwargs = {
            'members': {'required': False},
            'requests': {'required': False}
            # 'podium_1_user': {'required': False},
            # 'podium_2_user': {'required': False},
            # 'podium_3_user': {'required': False},
            # 'podium_1_score': {'required': False},
            # 'podium_2_score': {'required': False},
            # 'podium_3_score': {'required': False}
        }

class PopulatedGroupSerializer(GroupSerializer):

    owner = UserSerializer()
    members = UserSerializer(many=True)
    requests = UserSerializer(many=True)


class TownSerializer(serializers.ModelSerializer):

    class Meta:
        model = Town
        fields = ('id', 'name', 'name_ascii', 'lat', 'lng', 'country', 'iso2', 'iso3', 'continent', 'admin_name', 'capital', 'population', 'visitors')
        extra_kwargs = {
            'iso2': {'required': False}, 
            'iso3': {'required': False}, 
            'admin_name': {'required': False},
            'capital': {'required': False},
            'population': {'required': False},
            'visitors': {'required': False}
        }