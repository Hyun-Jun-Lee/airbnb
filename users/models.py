from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = ((GENDER_MALE, "Male"), (GENDER_FEMALE, "Female"))

    LANGUAGE_ENGLISH = "En"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "En"), (LANGUAGE_KOREAN, "Kr"))

    CURRNECY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRNECY_USD, "usd"), (CURRENCY_KRW, "krw"))

    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, null=True, blank=True
    )
    bio = models.TextField(default="", blank=True)
    birth = models.DateField(null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, null=True, blank=True, max_length=2
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, null=True, blank=True, max_length=3
    )

    superhost = models.BooleanField(default=False)
