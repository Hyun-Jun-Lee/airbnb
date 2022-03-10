from django.urls import path
from . import views

app_name = "conversations"

urlpatterns = [
    path("talk/<int:a_pk>/<int:b_pk>", views.talk_conversation, name="talk"),
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="detail"),
]
