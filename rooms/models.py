from django.db import models
from core import models as core_models
from django_countries.fields import CountryField
from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    pass


class Amenity(AbstractItem):
    pass


class Facility(AbstractItem):
    pass


class HouseRule(AbstractItem):
    pass


class Room(core_models.TimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(max_length=50)
    description = models.TextField()
    country = CountryField()
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

    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    house_rule = models.ManyToManyField(HouseRule, blank=True)

    def __str__(self):
        return self.name


class Photo(core_models.TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    caption = models.CharField(max_length=50)
    file = models.ImageField()

    def __str__(self):
        return self.caption
