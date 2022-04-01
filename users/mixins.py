from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# 소스코드 : https://github.com/django/django/blob/main/django/contrib/auth/mixins.py
# document : https://docs.djangoproject.com/en/4.0/topics/auth/default/


class LoggedOutOnlyView(UserPassesTestMixin):
    # text_fucn() method가 False를 리턴하면 permission error와 함께 요청을 거절
    def test_func(self):
        return not self.request.user.is_authenticated

    # AccessMixins에서 오버라이드
    # protect url path, url router로 접근하려 할 때 메세지
    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


# 인증되지 않은 유저의 request를 login_url로 보내거나 HTTP 403 Forbidden error를 보여준다.
class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")
