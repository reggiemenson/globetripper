from typing import Optional

import jwt

from django.conf import settings
from rest_framework.request import Request

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_204_NO_CONTENT

from .badge_logic import get_platform_badges, get_user_badges, get_user_score
from .models import User
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


class ProfileView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serialized_user = PopulatedUserSerializer(user)
        return Response(serialized_user.data)

        # limited edit user path.

    def put(self, request):
        initial_user = User.objects.get(pk=request.user.id)
        updated_user = UserSerializer(initial_user, data=request.data)
        if updated_user.is_valid():
            initial_user = updated_user
            initial_user.save()
            return Response(initial_user.data)
        return Response(updated_user.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request):
        user = User.objects.get(pk=request.user.id)
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)

        # The following view is for editing the user preference points (badges, towns, etc) that will affect ranking.


class EditDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    def put(self, request):
        initial_user = User.objects.get(pk=request.user.id)
        updated_user = UserSerializer(initial_user, data=request.data)
        if updated_user.is_valid():
            initial_user = updated_user
            initial_user.save()
            new_user = User.objects.get(pk=request.user.id)
            user_data = PopulatedUserSerializer(new_user)

            badges = get_user_badges(user_data)
            score = get_user_score(user_data)

            test_user = User.objects.get(pk=request.user.id)
            test_user.score = score
            badge_user = UserSerializer(test_user)
            badge_user.data['badges'].clear()
            badge_user.data['badges'].extend(badges)

            updated_badge_user = UserSerializer(test_user, data=badge_user.data)
            if updated_badge_user.is_valid():
                test_user = updated_badge_user
                test_user.save()

                all_users = User.objects.all()
                serialized_users = PopulatedUserSerializer(all_users, many=True)
                get_platform_badges(serialized_users)

                return Response(test_user.data)
            return Response(updated_badge_user.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(updated_user.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class UserView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serialized_user = PopulatedUserSerializer(user)
        return Response(serialized_user.data)
    

class UserListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        users = User.objects.all()
        serialized_users = PopulatedUserSerializer(users, many=True)
        return Response(serialized_users.data)
