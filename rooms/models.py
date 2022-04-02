from email.policy import default
from django.utils import timezone
from dateutil import relativedelta
from django.db import models
from django.urls import reverse
from core import models as core_models
from django_countries.fields import CountryField
from users import models as user_models
from calend import Calendar

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    name = models.CharField(max_length=50)
    # abstract = True로 설정하면 해당 클래스는 DB 테이블을 가지지 않고
    # 이 클래스를 상속 받은 자식 클래스들이 실체가 있는 DB 테이블이 된다.
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# admin 채널에서 직접 추가 가능
class RoomType(AbstractItem):
    # verbose_name : admin에서 보일 이름
    pass


class Amenity(AbstractItem):
    pass


class Facility(AbstractItem):
    pass


class HouseRule(AbstractItem):
    pass


class Photo(core_models.TimeStampedModel):
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)
    caption = models.CharField(max_length=50)
    file = models.ImageField(upload_to="room_photos")

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(max_length=50)
    description = models.TextField()
    country = CountryField(default="KR")
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

    # on_delete는 ForeignKey에만 쓰임(ForeignKey는 한가지에만 연결되기 때문에)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    # 오직 하나만 필요한 경우 foreign key를 사용하지만 여러개가 필요한 경우 ManyToMany를 사용
    # related_name : 역참조 대상인 객체를 부를 때 이름(원래는 [class_name]_set으로 접근)
    amenities = models.ManyToManyField(Amenity, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    house_rule = models.ManyToManyField(HouseRule, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_ratings = 0
        all_reviews = self.reviews.all()
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_avg()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        today = timezone.localtime(timezone.now()).date()
        this_month = Calendar(today.year, today.month)
        nextmonth = today + relativedelta.relativedelta(months=1)
        next_month = Calendar(nextmonth.year, nextmonth.month)
        return [this_month, next_month]
