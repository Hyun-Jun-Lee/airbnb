from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

# Create your models here.


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField(
        user_models.User, related_name="conversation", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ",".join(usernames)

    def count_message(self):
        return self.message.count()
    
    def count_participants(self):
        return self.participants.count()


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey(
        user_models.User, related_name="message", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        Conversation, related_name="message", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says : {self.message}"
