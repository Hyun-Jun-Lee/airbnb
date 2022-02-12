from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

# Create your models here.


class List(core_models.TimeStampedModel):

    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        user_models.User, related_name="lists", on_delete=models.CASCADE
    )
    room = models.ManyToManyField(room_models.Room, related_name="lists")

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.room.count()
