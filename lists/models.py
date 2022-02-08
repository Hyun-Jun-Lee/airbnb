from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

# Create your models here.


class List(core_models.TimeStampedModel):

    name = models.CharField(max_length=50)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    room = models.ForeignKey(room_models.Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
