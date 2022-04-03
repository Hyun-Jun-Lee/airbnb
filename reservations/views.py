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


class AlreadyReserved(Exception):
    pass


def create_reservation(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        # BookeDay가 있으면 예약이 안되므로 AlreadyReserved
        check_booked = models.BookedDay.objects.get(
            day=date_obj, reservation__room=room
        )
        if check_booked is not None:
            raise AlreadyReserved()
    except (room_models.Room.DoesNotExist, AlreadyReserved):
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

        if reservation is None:
            raise Http404("Invalid access")

        if (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404("Neither guest or host.")

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


class ReservationListView(mixins.LoggedInOnlyView, ListView):

    template_name = "reservations/reservation_list.html"
    context_object_name = "reservation_list"

    # coustomize queryset, 위에서 지정한 context name로 전달됨
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
