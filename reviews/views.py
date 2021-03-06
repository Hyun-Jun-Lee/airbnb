from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic import ListView
from rooms import models as room_models
from . import forms, models
from users import mixins

# Create your views here.


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            # CreateReviewForm에서 생성된 objects 가져오기
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
