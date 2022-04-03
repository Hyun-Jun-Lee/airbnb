from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room>/<int:year>-<int:month>-<int:day>",
        views.create_reservation,
        name="create",
    ),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path("<int:pk>/<str:verb>", views.edit_reservation, name="edit"),
    path(
        "reservation_list/",
        views.ReservationListView.as_view(),
        name="reservation_list",
    ),
    path(
        "<int:pk>/reservation_list_host/",
        views.reservation_list_host,
        name="reservation_list_host",
    ),
]
