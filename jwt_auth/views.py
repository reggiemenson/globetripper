from jwt_auth.serializers import UserSerializer, PopulatedUserSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from django.conf import settings
import jwt

from django.db.models import F

from .badge_logic import get_platform_badges, get_user_badges, get_user_score
from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers import ValidateSerializer, UserSerializer, PopulatedUserSerializer 

class RegisterView(APIView):

    # def get_user(self, request):
    #     serializer = ValidateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'Registration successful'})

    #     return Response(serializer.errors, status=422)

    def post(self, request):
        serializer = ValidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'})

        return Response(serializer.errors, status=422)


class LoginView(APIView):

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({'message': 'Invalid credentials'})

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = self.get_user(email)
        if not user.check_password(password):
            raise ValidationError({'message': 'Invalid credentials'})

        token = jwt.encode(
            {'sub': user.id}, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token, 'message': f'Welcome {user.username}!'})


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
        if (updated_user.is_valid()):
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
        if (updated_user.is_valid()):
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
            if (updated_badge_user.is_valid()):
                test_user = updated_badge_user
                test_user.save()

                all_users = User.objects.all()
                serialized_userList = PopulatedUserSerializer(all_users, many=True)
                get_platform_badges(serialized_userList)

                return Response(test_user.data)
            return Response(updated_badge_user.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(updated_user.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class UserView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serialized_user = PopulatedUserSerializer(user)
        return Response(serialized_user.data)


    # def post(self, request, pk): 
    #         request.data['owner'] = request.user.id 
    #         request.data['post'] = pk # attach the post id from the url to comment
    #         town = TownSerializer(data=request.data) # serialize the comment
    #         if town.is_valid(): # if the comment is valid
    #             town.save() # save the comment
    #         return Response(town.errors, status=HTTP_422_UNPROCESSABLE_ENTITY) # send back any errors from the comment if it wasnt valid

    

class UserListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        print('reached?')
        users = User.objects.all()
        serialized_userList = PopulatedUserSerializer(users, many=True)
        return Response(serialized_userList.data)


         
