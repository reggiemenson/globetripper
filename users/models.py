from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import VisitorManager, CustomUserManager


class User(AbstractUser):
    objects = CustomUserManager()
    travellers = VisitorManager()

    ORIENTATION = (
        ("LH", "Left-Handed"),
        ("RH", "Right-Handed"),
    )

    email = models.CharField(max_length=50, unique=True)
    image = models.CharField(max_length=500, default="https://bit.ly/37UONby")
    score = models.IntegerField(default=0)
    dexterity = models.CharField(max_length=2, choices=ORIENTATION, default="RH")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def add_visits(self, *objs) -> None:
        self.towns.add(*objs)
        self.add_awards()

    def add_awards(self) -> None:
        awarded_badges = self.badges.model.objects.get_qualifying_badges(
            towns=self.towns
        )
        self.badges.add(*awarded_badges)
        self.score = self.towns.count_travel_score()
        self.save()
