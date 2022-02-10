from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models
from django.utils import timezone

# Create your models here.


class Reservation(core_models.TimeStampedModel):

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CANCELED, "Canceled"),
        (STATUS_CONFIRMED, "Confirmed"),
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    check_in = models.DateField()
    check_out = models.DateField()

    guest = models.ForeignKey(
        user_models.User, related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        room_models.Room, related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in} - {self.check_out}"

    def in_prograss(self):
        now = timezone.now().date()
        return now > self.check_in and now < self.check_out

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out
