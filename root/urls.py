from django.urls import path, include
from .views import Index, Login, LogoutView, SignUp, ideas 
from .api_views import IdeaViewSet, WhatsNewViewSet

from rest_framework import routers
from rest_framework.negotiation import BaseContentNegotiation

app_name = "root"

urlpatterns = [
  
    path("index/", Index.as_view(), name="index"),
    path("ideas/", ideas, name="ideas"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("sign_up/", SignUp.as_view(), name="sign_up"),
]


router = routers.SimpleRouter()
router.register(r'ideas', IdeaViewSet)
router.register(r'whatsnews', WhatsNewViewSet)

api_urlpatterns = [
    path("root/", include((router.urls, "root-api")))
]