from urllib import request
from django.shortcuts import redirect, render
from django.views.generic import ListView
from . import models

# Create your views here.


class HomeView(ListView):
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    
