from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from . import models
from math import ceil
from django.core.paginator import Paginator, EmptyPage

# Create your views here.


def all_room(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(int(page))
        return render(
            request,
            "rooms/home.html",
            {"page": rooms},
        )
    except EmptyPage:
        return redirect("/")
