from django.db import models
from core import models as core_models
from django_countries.fields import CountryField
from users import models as user_models

# Create your models here.


class Room(core_models.TimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(max_length=50)
    description = models.TextField()
    counrty = CountryField()
    city = models.CharField(max_length=50)
    price = models.IntegerField()
    adress = models.CharField(max_length=100)
    beds = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
