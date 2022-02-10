from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    fieldsets = (
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces Detail", {"fields": ("amenities", "facilities", "house_rule")}),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = [
        "name",
        "country",
        "city",
        "price",
        "address",
        "beds",
        "baths",
        "guests",
        "check_in",
        "check_out",
        "instant_book",
        "count_photos",
        "total_rating",
    ]

    list_filter = ["city", "country", "instant_book"]

    search_fields = ["city", "^host__username"]

    filter_horizontal = ["amenities", "facilities", "house_rule"]

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
