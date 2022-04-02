from django.db import models
from . import managers

# Create your models here.

# 반복적인 작업
class TimeStampedModel(models.Model):
    # auto_now_add = 처음 생성 시간, auto_now : 수정 될 때마다 시간 업데이트
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    # database로 가지 않고 다른 모델에서 쓰일 때 database에 적재되게 만들기
    class Meta:
        # abstarct : database에 나타나지 않는 model, 단순 기능만 사용
        abstract = True
