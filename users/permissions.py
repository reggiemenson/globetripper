from rest_framework import permissions


class ListOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in {'list'}:
            return True


class DetailOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in {'detail'}:
            return True