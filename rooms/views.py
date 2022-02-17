from time import timezone
from django.utils import timezone
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from . import models

# Create your views here.


class HomeView(ListView):
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):
    model = models.Room


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         return redirect(reverse("core:home"))
