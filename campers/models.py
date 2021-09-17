from django.db import models

from django.db.models import FloatField


class Camper(models.Model):
    latitude = FloatField()
    longitude = FloatField()
