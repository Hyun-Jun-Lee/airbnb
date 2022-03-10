from django.db import models
from . import managers

# Create your models here.


class TimeStampedModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    # database로 가지 않고 다른 모델에서 쓰일 때 database에 적재되게 만들기
    class Meta:
        # abstarct : database에 나타나지 않는 model
        abstract = True
