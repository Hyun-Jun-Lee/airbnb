from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("sigup/", views.SignUpView.as_view(), name="signup"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("update_profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update_password/", views.UpdatePasswordView.as_view(), name="password"),
]
