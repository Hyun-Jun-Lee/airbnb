from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    pass


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
    ]

    list_filter = ["city", "country", "instant_book"]

    search_fields = ["city", "^host__username"]

    filter_horizontal = ["amenities", "facilities", "house_rule"]


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
