from time import timezone
from urllib import request
from django.utils import timezone
from django.shortcuts import redirect, render
from django.views.generic import ListView
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
