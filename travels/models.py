from django.db import models

# THIS IS THE CODE FOR IMPORTING THE USER MODEL WHEN READY
from django.contrib.auth import get_user_model
User = get_user_model()


# MODELS BELOW

class Town(models.Model):
    name = models.CharField(max_length=255)
    name_ascii = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    iso2 = models.CharField(max_length=255, null=True)
    iso3 = models.CharField(max_length=255, null=True)
    admin_name = models.CharField(max_length=255, null=True)
    capital = models.CharField(max_length=255, null=True)
    population = models.IntegerField(null=True)
    continent = models.CharField(max_length=255)
    visitors = models.ManyToManyField(
        User,
        related_name='towns',
        blank=True
    )

    def __str__(self):
        return f'{self.name} - {self.country}'


class Trip(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    towns = models.ManyToManyField(
        Town,
        related_name='trips',
        blank=True
    )
    notes = models.CharField(max_length=5000, null=True)
    owner = models.ForeignKey(
        User,
        related_name='trips',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name}, {self.start_date}/{self.end_date}'


class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=100)
    users = models.ManyToManyField(
        User,
        related_name='badges',
        blank=True
    )

    def __str__(self):
        return f'{self.name}'


class Group(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=500, default='https://cdn.pixabay.com/photo/2014/04/02/10/47/globe-304586_1280.png')
    owner = models.ForeignKey(
        User,
        related_name='groups_owned',
        on_delete=models.CASCADE,
        default=1
    )
    members = models.ManyToManyField(
        User,
        related_name='groups_joined',
        blank=True
    )
    requests = models.ManyToManyField(
        User,
        related_name='groups_requested',
        blank=True
    )
    podium_1_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='groups_podium1',
        blank=True,
        null=True
    )
    podium_2_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='groups_podium2',
        blank=True,
        null=True
    )
    podium_3_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='groups_podium3',
        blank=True,
        null=True
    )
    podium_1_score = models.IntegerField(null=True, blank=True)
    podium_2_score = models.IntegerField(null=True, blank=True)
    podium_3_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Image(models.Model):
    image = models.CharField(max_length=100)
    trip = models.ForeignKey(  # One to many with Posts as well, A Post can have many comments, but a comment can only belong to one Post
        Trip,
        on_delete=models.SET_NULL,
        related_name='images',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.image}'
