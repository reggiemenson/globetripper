from django.db import models

from travels.managers import BadgeAssignmentManager, TownManager
from users.models import User


class Town(models.Model):
    objects = TownManager()

    name = models.CharField(max_length=255)
    # maybe change name
    name_ascii = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    iso2 = models.CharField(max_length=255, null=True)
    iso3 = models.CharField(max_length=255, null=True)
    admin_name = models.CharField(max_length=255, null=True)
    capital = models.CharField(max_length=255, null=True)
    population = models.IntegerField(null=True)
    continent = models.CharField(max_length=255)
    visitors = models.ManyToManyField(User, related_name="towns", blank=True)

    def __str__(self):
        return f"{self.name} - {self.country}"


class Trip(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    towns = models.ManyToManyField(Town, related_name="trips", blank=True)
    notes = models.TextField(null=True)
    owner = models.ForeignKey(User, related_name="trips", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.start_date}/{self.end_date}"


class Badge(models.Model):
    objects = BadgeAssignmentManager()

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="badges", blank=True)

    def __str__(self):
        return f"{self.name}"


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.CharField(
        max_length=500,
        default="https://cdn.pixabay.com/photo/2014/04/02/10/47/globe-304586_1280.png",
    )
    owner = models.ForeignKey(
        User, related_name="groups_owned", on_delete=models.CASCADE, default=1
    )
    members = models.ManyToManyField(User, related_name="groups_joined", blank=True)
    # may review
    requests = models.ManyToManyField(User, related_name="groups_requested", blank=True)
    # the rest of fields are calculated fields
    podium_1_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="groups_podium1",
        blank=True,
        null=True,
    )
    podium_2_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="groups_podium2",
        blank=True,
        null=True,
    )
    podium_3_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="groups_podium3",
        blank=True,
        null=True,
    )
    podium_1_score = models.IntegerField(null=True, blank=True)
    podium_2_score = models.IntegerField(null=True, blank=True)
    podium_3_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    image = models.CharField(max_length=100)
    trip = models.ForeignKey(
        Trip, on_delete=models.SET_NULL, related_name="images", blank=True, null=True
    )

    def __str__(self):
        return f"{self.image}"
