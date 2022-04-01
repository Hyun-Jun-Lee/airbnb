from django.db import models
from django.contrib.auth.models import UserManager


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


# UserManager은 BaseUserManager을 상속 받고 있음
# https://github.com/django/django/blob/main/django/contrib/auth/models.py
class CustomUserManager(CustomModelManager, UserManager):
    pass
