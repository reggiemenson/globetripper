from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_202_ACCEPTED
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from users.models import User

from .models import Town, Badge, Trip, Group
from .serializers import TripSerializer, BadgeSerializer, PopulatedGroupSerializer, TownSerializer, GroupSerializer, PopulatedBadgeSerializer, PopulatedTripSerializer, TownSerializer

# TownsView
# /towns
# GET all towns: list all towns


class TownsView(APIView):

    def get(self, request):
        towns = Town.objects.all()
        serializer = TownSerializer(towns, many=True,)

        return Response(serializer.data)


# # CountriesView
# # /countries
# # GET all countries and number of users who visited

# class CountriesView(APIView):

#     def get(self, request):
#         towns = Town.objects.all()
#         serialized_towns = PopulatedTownSerializer(towns, many=True)
#         print(serialized_towns.data)

#         all_user_countries = list(map(lambda town: town['country'], serialized_towns.data))
#         unique_user_countries = set(all_user_countries)

#         return Response(unique_user_countries)

# BadgesView
# /badges
# GET all badges: list all badges

class BadgesView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, _request):
        badges = Badge.objects.all()
        serialized_badges = PopulatedBadgeSerializer(badges, many=True)
        return Response(serialized_badges.data)


# IndividualBadgeView
# /badges/pk
# PUT badge: posts a user to that badge

class IndividualBadgeView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, _request, pk):
        badge = Badge.objects.get(pk=pk)
        serialized_badge = PopulatedBadgeSerializer(badge)
        return Response(serialized_badge.data)

    # def put(self, request, pk):
    #     request.data['owner'] = request.user.id
    # # Not sure about this -  we want to select any user -not just the one who is requesting?

    #     badge = Badge.objects.get(pk=pk)
    #     updated_badge = PopulatedBadgeSerializer(
    #         badge, data=request.user.id)  # User ID or just User??
    #     if updated_badge.is_valid():
    #         updated_badge.save()
    #         return Response(updated_badge.data)
    #     return Response(updated_badge.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


# TripsView
# /trips
# POST all cities: user posts a trip

class TripsView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, _request):
        trips = Trip.objects.all()
        serialized_trips = PopulatedTripSerializer(trips, many=True)
        return Response(serialized_trips.data)
#this just gets all trips, but have realised we probably want it to be just the user's trips?

    def post(self, request):
        request.data['owner'] = request.user.id
        trip = TripSerializer(data=request.data)
        if trip.is_valid():
            trip.save()
            return Response(trip.data, status=HTTP_201_CREATED)
        return Response(trip.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


# IndividualTripView
# /trips/pk
# PUT, DEL: allow user to alter trip detail if they are the owner

class IndividualTripView(APIView):

    def put(self, request, pk):
        request.data['owner'] = request.user.id
    # Not sure about this -  we want to select any user -not just the one who is requesting?

        trip = Trip.objects.get(pk=pk)
        updated_trip = PopulatedTripSerializer(
            trip, data=request.user.id)  # User ID or just User??
        if updated_trip.is_valid():
            updated_trip.save()
            return Response(updated_trip.data)
        return Response(updated_trip.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, comment_pk, **kwargs): 
        trip = Trip.objects.get(pk=comment_pk) 
        if trip.owner.id != request.user.id:
            return Response(status=HTTP_401_UNAUTHORIZED)
        trip.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# GroupsView
# /groups
# GET all groups: overview of all groups (for search)
# POST all groups: user posts a new group and becomes owner

class GroupsView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        groups = Group.objects.all()
        serializer = PopulatedGroupSerializer(groups, many=True)

        return Response(serializer.data)

    def post(self, request):
        request.data['owner'] = request.user.id
        request.data['members'] = (request.user.id, )
        group = GroupSerializer(data=request.data)
        if group.is_valid():
            group.save()
            return Response(group.data, status=HTTP_201_CREATED)
        return Response(group.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

# IndividualGroupView
# /groups/pk
# GET group: get individual group
# PUT, DEL: allow user to alter group if they are the owner

class IndividualGroupView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        group = Group.objects.get(pk=pk)
        serializer = PopulatedGroupSerializer(group)

        return Response(serializer.data)

    def put(self, request, pk):
        request.data['owner'] = request.user.id
        group = Group.objects.get(pk=pk)
        updated_group = GroupSerializer(group, data=request.data)
        if (updated_group.is_valid()):
            group = updated_group
            group.save()
            return Response(group.data)
        return Response(updated_group.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        group = Group.objects.get(pk=pk)
        if group.owner.id != request.user.id:
            return Response(status=HTTP_401_UNAUTHORIZED)
        group.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# GroupMembershipView
# groups/pk/membership
# GET: allow any user to request membership (that isn't alraedy a user)
# PUT: allow group owner to approve membership
# DELETE: allow group owner or member to revoke membership

class GroupMembershipView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        requester = User.objects.get(pk=request.user.id)
        group = Group.objects.get(pk=pk)

        if requester in group.members.all():
            return Response('User already a member', status=HTTP_422_UNPROCESSABLE_ENTITY)
        
        group.requests.add(requester)
        group.save()
        return Response(status=HTTP_202_ACCEPTED)


    def put(self, request, pk):
        group = Group.objects.get(pk=pk)
        if group.owner.id != request.user.id:
            return Response(status=HTTP_401_UNAUTHORIZED)
        requester = User.objects.get(pk=request.data['id'])
        if requester not in group.requests.all():
            return Response('User did not request to join', status=HTTP_422_UNPROCESSABLE_ENTITY)
        
        group.requests.remove(requester)
        group.members.add(requester)

        group.save()
        return Response(status=HTTP_202_ACCEPTED)


    def delete(self, request, pk):
        requester = User.objects.get(pk=request.user.id)
        group = Group.objects.get(pk=pk)
        deletee = User.objects.get(pk=request.data['id'])

        if (group.owner.id != request.user.id) and (requester.id != deletee.id) and (requester not in group.members.all()):
            return Response(status=HTTP_401_UNAUTHORIZED)

        group.members.remove(deletee)
        group.save()

        return Response(status=HTTP_202_ACCEPTED)
