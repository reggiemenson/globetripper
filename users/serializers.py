from rest_framework import serializers
from travels.serializers import (
    TownSerializer,
    TripSerializer,
    BadgeSerializer,
    GroupSerializer,
)
from users.models import User

import django.contrib.auth.password_validation as validations
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError


class ValidateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.pop("password")
        password_confirmation = data.pop("password_confirmation")

        if password != password_confirmation:
            raise serializers.ValidationError(
                {"password_confirmation": "Passwords do not match"}
            )

        try:
            validations.validate_password(password=password)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})

        data["password"] = make_password(password)
        return data

        # input the required fields in the serializer. The serializer is used for the fields requested on the route.

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "dexterity",
            "image",
            "email",
            "password",
            "password_confirmation",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "dexterity",
            "score",
            "image",
            "towns",
            "badges",
            "groups_owned",
            "groups_requested",
            "groups_joined",
            "groups_podium1",
            "groups_podium2",
            "groups_podium3",
        )
        extra_kwargs = {
            "score": {"required": False},
            "towns": {"required": False},
            "badges": {"required": False},
            "groups_owned": {"required": False},
            "groups_joined": {"required": False},
            "groups_requested": {"required": False},
            "groups_podium1": {"required": False},
            "groups_podium2": {"required": False},
            "groups_podium3": {"required": False},
        }


class PopulatedUserSerializer(serializers.ModelSerializer):
    towns = TownSerializer(many=True)
    badges = BadgeSerializer(many=True)
    groups_owned = GroupSerializer(many=True)
    groups_requested = GroupSerializer(many=True)
    groups_joined = GroupSerializer(many=True)
    groups_podium1 = GroupSerializer(many=True)
    groups_podium2 = GroupSerializer(many=True)
    groups_podium3 = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "dexterity",
            "score",
            "image",
            "towns",
            "badges",
            "groups_owned",
            "groups_requested",
            "groups_joined",
            "groups_podium1",
            "groups_podium2",
            "groups_podium3",
        )
