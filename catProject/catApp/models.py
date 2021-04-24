from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime


lootTypes = [
    "rat",
    "mouse",
    "bird",
    "fish",
    "catnip",
    "meat",
    "bone",
    "leftovers",
    "other",
]
bodyColors = [
    "white",
    "black",
    "brown",
    "grey",
    "ginger",
    "cream",
    "fawn",
    "mulit-color",
    "other",
]


def validate_owner(owner):
    cats = Cat.objects.filter(owner=owner)
    if cats.count() >= 4:
        raise ValidationError("User can have only 4 cats.")


class Cat(models.Model):
    COLOR_CHOICES = (
        ("1", "white"),
        ("2", "black"),
        ("3", "brown"),
        ("4", "grey"),
        ("5", "ginger"),
        ("6", "cream"),
        ("7", "fawn"),
        ("8", "multi-color"),
        ("9", "other"),
    )
    name = models.CharField(max_length=40)
    bodyColor = models.CharField(max_length=12, choices=COLOR_CHOICES)
    gender = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, related_name="cats", on_delete=models.CASCADE, validators=[validate_owner]
    )

    def __str__(self):
        return self.name


class Hunting(models.Model):
    dateStart = models.DateTimeField(auto_now=False, auto_now_add=False)
    dateEnd = models.DateTimeField(auto_now=False, auto_now_add=False)
    hunter = models.ForeignKey(Cat, related_name="hunters", on_delete=models.CASCADE)

    def clean(self):
        if self.dateEnd < self.dateStart:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return (
            self.dateStart.strftime("%d-%m-%YT%H:%M:%S")
            + " - "
            + self.dateEnd.strftime("%d-%m-%YT%H:%M:%S")
            + " "
            + str(self.hunter)
        )


class Loot(models.Model):
    lootType = models.CharField(max_length=10)
    hunting = models.ForeignKey(Hunting, related_name="loots", on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, related_name="cat_loots", on_delete=models.CASCADE)

    def clean(self):
        if self.cat != self.hunting.hunter:
            raise ValidationError("Cat, hunting and loot must match the same cat.")
        elif self.lootType not in lootTypes:
            raise ValidationError(
                "Invalid loot type. Must be the one from " + str(lootTypes)
            )

    def __str__(self):
        return self.lootType


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
