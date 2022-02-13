from django.contrib import admin
from . import models
from django.utils.html import mark_safe

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    fieldsets = (
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces Detail", {"fields": ("amenities", "facilities", "house_rule")}),
        ("Last Details", {"fields": ("host",)}),
    )

    inlines = (PhotoInline,)

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
        "count_amenities",
    ]

    raw_id_fields = ("host",)

    list_filter = ["city", "country", "instant_book"]

    search_fields = ["city", "^host__username"]

    filter_horizontal = ["amenities", "facilities", "house_rule"]

    def count_photos(self, obj):
        return obj.photos.count()

    def count_amenities(self, obj):
        return obj.amenities.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="60px" src="{obj.file.url}">')
