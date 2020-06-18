from django.urls import path, include
from .api_views import IdeaViewSet, WhatsNewViewSet

from rest_framework import routers
from rest_framework.negotiation import BaseContentNegotiation

app_name = "root"

urlpatterns = [
]


router = routers.SimpleRouter()
router.register(r'ideas', IdeaViewSet)
router.register(r'whatsnews', WhatsNewViewSet)

api_urlpatterns = [
    path("root/", include((router.urls, "root-api")))
]