import re
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
    address = models.CharField(max_length=100)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )

    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rule = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def total_rating(self):
        all_ratings = 0
        all_reviews = self.reviews.all()
        for review in all_reviews:
            all_ratings += review.rating_avg()
        return all_ratings / len(all_reviews)


class Photo(core_models.TimeStampedModel):
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)
    caption = models.CharField(max_length=50)
    file = models.ImageField()

    def __str__(self):
        return self.caption
