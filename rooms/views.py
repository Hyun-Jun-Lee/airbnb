from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from . import models

# Create your views here.


def all_room(request):
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
