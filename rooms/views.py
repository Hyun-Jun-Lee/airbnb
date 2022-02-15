from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from . import models
from math import ceil
from django.core.paginator import Paginator

# Create your views here.


def all_room(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    return render(
        request,
        "rooms/home.html",
        {"rooms": rooms},
    )
