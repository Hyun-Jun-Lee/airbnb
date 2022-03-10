from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from core import managers as core_managers

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

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGING_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGING_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, null=True, blank=True
    )
    bio = models.TextField(default="", blank=True)
    birth = models.DateField(null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        default=LANGUAGE_KOREAN,
        null=True,
        blank=True,
        max_length=2,
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        default=CURRENCY_KRW,
        null=True,
        blank=True,
        max_length=3,
    )

    superhost = models.BooleanField(default=False)

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    objects = core_managers.CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
