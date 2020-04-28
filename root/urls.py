from django.urls import path
from .views import Index, Login, LogoutView, SignUp


app_name = "root"

urlpatterns = [
    path("index/", Index.as_view(), name="index"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("sign_up/", SignUp.as_view(), name="sign_up"),
]