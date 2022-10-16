from typing import Optional

import jwt

from django.conf import settings
from django.http import Http404
from rest_framework import viewsets
from rest_framework.request import Request

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from travels.utils import recalculate_platform_badges, UserVisits
from .models import User
from .permissions import ListOnly
from .serializers import ValidateSerializer, UserSerializer, PopulatedUserSerializer


class RegisterView(APIView):

    def post(self, request: Request) -> Response:
        serializer = ValidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Registration successful'})

        detail_dict = {
            'detail': serializer.errors
        }

        return Response(detail_dict, status=422)


class LoginView(APIView):

    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')
        user = self.get_user(email)

        if not user or user and not user.check_password(password):
            raise AuthenticationFailed()

        token = jwt.encode(
            {'sub': user.id}, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token, 'detail': f'Welcome {user.first_name}!'})

    @staticmethod
    def get_user(email) -> Optional[User]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PopulatedUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete']

    def get_object(self):
        if not self.request.user or not self.request.user.id:
            raise Http404
        return self.request.user

    def _update_object(self, data, partial=False):
        instance = self.get_object()
        serializer = UserSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return serializer.instance

    def update(self, request, *args, **kwargs):
        self.serializer_class = UserSerializer
        return super(ProfileViewSet, self).update(request, *args, **kwargs)

    def town_update(self, request, *args, **kwargs):
        updated_user = self._update_object(request.data)
        updated_user_info = UserVisits(updated_user.towns.all())
        award_data = {
            'badges': [badge.id for badge in updated_user_info.get_awarded_badges()],
            'score': updated_user_info.score,
        }
        awarded_serializer = UserSerializer(self._update_object(data=award_data, partial=True))
        recalculate_platform_badges()

        return Response(awarded_serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = PopulatedUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated | ListOnly]
    http_method_names = ['get']
