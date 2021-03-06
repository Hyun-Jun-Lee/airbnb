from time import timezone
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    DetailView,
    View,
    UpdateView,
    FormView,
    DeleteView,
)
from . import models, forms
from reservations import models as reservations_models
from users import mixins as user_mixins

# Create your views here.

# ListView는 자동으로 templates에서 {appname}_list 라는 파일 이름을 찾는다
class HomeView(ListView):
    model = models.Room
    paginate_by = 8
    paginate_orphans = 5
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):
    model = models.Room


class SearchView(View):
    def get(self, request):
        form = forms.SearchForm(request.GET)

        if form.is_valid():

            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filtering = {}

            if city != "Any City":
                filtering["city__startswith"] = city

            filtering["country"] = country

            if room_type is not None:
                filtering["room_type"] = room_type

            if min_price is not None and max_price is not None:
                filtering["price__gte"] = min_price
                filtering["price__lte"] = max_price

            if guests is not None:
                filtering["guests__gte"] = guests

            if bedrooms is not None:
                filtering["bedrooms__gte"] = bedrooms

            if beds is not None:
                filtering["beds__gte"] = beds

            if baths is not None:
                filtering["baths__gte"] = baths

            if superhost is True:
                filtering["host__superhost"] = True

            for amenity in amenities:
                filtering["amenities"] = amenity

            for facility in facilities:
                filtering["facilities"] = facility

            # ** : unpack
            qs = models.Room.objects.filter(**filtering).order_by("-created")

            paginator = Paginator(qs, 10, orphans=5)

            page = request.GET.get("page", 1)

            rooms = paginator.get_page(page)

            return render(request, "rooms/search.html", {"form": form, "rooms": rooms})
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
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
    # room_edit.html로 room context 전달
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        photo = models.Photo.objects.get(pk=photo_pk)

        if room.host.pk != user.pk:
            if not (room.host.pk == user.pk and user.pk == photo.room.pk):
                messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    # form에서 Meta 메서드로 받아왓기 때문에 없어도 됨
    # model = models.Photo
    # fields = ("caption", "file")
    template_name = "rooms/photo_add.html"
    form_class = forms.CreatePhotoForm

    # form_valid do not use with SuccessMessageMixin
    # form에 pk를 보내는 역활
    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        # form에서 저장한 room 받아오기
        room = form.save()
        # room.host 현재 사용자로 변경 후 저장
        room.host = self.request.user
        room.save()
        # it can user after save()
        form.save_m2m()
        messages.success(self.request, "Room Uploaded")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


@login_required
def delete_room(request, pk):
    try:
        room = get_object_or_404(models.Room, pk=pk)

        if request.user.pk != room.host.pk:
            raise Http404("Can't Delete This Room")

        room.delete()
        messages.success(request, f"{room.name} Delete Complete")
        return redirect(reverse("core:home"))
    except models.Room.DoesNotExist:
        messages.error(request, "Can't Delete This Room")
        return redirect(reverse("core:home"))


@login_required
def room_like(request, room_pk):
    if request.user.is_authenticated:
        room = get_object_or_404(models.Room, pk=room_pk)

        if room.like_users.filter(pk=request.user.pk).exists():
            room.like_users.remove(request.user)
            room.like_count -= 1
            room.save()
        else:
            room.like_users.add(request.user)
            room.like_count += 1
            room.save()
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
    else:
        return redirect(reverse("core:home"))
