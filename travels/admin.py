from django.contrib import admin
from .models import Town, Trip, Badge, Group

# Register your models here.
admin.site.register(Town)
admin.site.register(Trip)
admin.site.register(Badge)
admin.site.register(Group)
