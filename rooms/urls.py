from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("create/", views.CreateRoomView.as_view(), name="create"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("like/<int:room_pk>/", views.room_like, name="like"),
    path("<int:pk>/delete/", views.delete_room, name="delete"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete_photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit_photo",
    ),
    path("<int:pk>/photos/add", views.AddPhotoView.as_view(), name="add_photo"),
]
