from django.http import Http404
from django.shortcuts import redirect, reverse, render
from django.views.generic import DetailView, View
from django.db.models import Q
from users import models as user_models
from . import models

# Create your views here.


def talk_conversation(request, a_pk, b_pk):
    a_user = user_models.User.objects.get_or_none(pk=a_pk)
    b_user = user_models.User.objects.get_or_none(pk=b_pk)
    if a_user is not None and b_user is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=a_user) & Q(participants=b_user)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(a_user, b_user)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


# class ConversationDetailView(DetailView):
#     # DetailView find 'pk' automatically

#     model = models.Conversation


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
