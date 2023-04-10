from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, blank=True)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.FloatField()


class PerevalAdded(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW'
        PENDING = 'PND'
        ACCEPTED = 'ACC'
        REJECTED = 'RJT'

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, blank=True)
    connect = models.CharField(max_length=255, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level_winter = models.CharField(max_length=2, blank=True)
    level_summer = models.CharField(max_length=2, blank=True)
    level_autumn = models.CharField(max_length=2, blank=True)
    level_spring = models.CharField(max_length=2, blank=True)
    status = models.CharField(choices=Status.choices, default=Status.NEW, max_length=3)


class Image(models.Model):
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='%Y/%m/%d')
    title = models.CharField(max_length=255)
