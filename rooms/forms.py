from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    # city = forms.CharField(initial="Any City")
    # .values() : 해당 필드 key,value / .values(): 튜플 형태, flat() : value의 리스트 형태
    city = forms.ModelChoiceField(
        required=True,
        queryset=models.Room.objects.all().values_list("city", flat=True),
    )
    country = CountryField(default="KR").formfield()
    min_price = forms.IntegerField(required=False, initial=10)
    max_price = forms.IntegerField(required=False, initial=1000)
    # queryset : 모델에서 데이터 가져와 선택
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any Type", queryset=models.RoomType.objects.all()
    )
    guests = forms.IntegerField(required=False, initial=1)
    bedrooms = forms.IntegerField(required=False, initial=1)
    beds = forms.IntegerField(required=False, initial=1)
    baths = forms.IntegerField(required=False, initial=1)
    superhost = forms.BooleanField(required=False, initial=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        # widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        # widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rule",
        )

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        # form 밖으로 room 내보내기
        return room
