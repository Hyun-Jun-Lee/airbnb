import datetime
from django.views.generic import View, ListView
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from reviews import forms as review_forms
from . import models
from users import mixins

# Create your views here.


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        # BookeDay가 있으면 예약이 안되므로 CreateError
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        form = review_forms.CreateReviewForm()
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        return render(
            self.request,
            "reservations/reservation_detail.html",
            {"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


# def reservation_list(request):
#     reservation_list = models.Reservation.objects.filter(guest=request.user)
#     return render(
#         request,
#         "reservations/reservation_list.html",
#         {"reservation_list": reservation_list},
#     )


class ReservationListView(mixins.LoggedInOnlyView, ListView):

    template_name = "reservations/reservation_list.html"
    context_object_name = "reservation_list"

    # model = models.Reservation 이렇게 하면 모든 reservation이 가져와짐
    # get_queryset 메서드로 설정하거나 queryset이라는 field로 정의 가능
    def get_queryset(self):
        qs = models.Reservation.objects.filter(guest=self.request.user)
        return qs


def reservation_list_host(request, pk):
    reservations = models.Reservation.objects.filter(room__host=pk)
    my_room = []

    # protect path
    for reservation in reservations:
        if reservation.room.host != request.user:
            raise Http404
        if reservation.room not in my_room:
            my_room.append(reservation.room)

    return render(
        request,
        "reservations/reservation_list_host.html",
        {"my_room": my_room, "reservations": reservations},
    )
