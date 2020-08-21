from django.urls import path, include
from . import api_views


from rest_framework import routers
from rest_framework_nested import routers

app_name = "home"

router = routers.SimpleRouter()
router.register(r'idea_categories', api_views.IdeaCategoryViewSet)
router.register(r'create_user', api_views.CreateUserView)

ideas_router = routers.NestedSimpleRouter(router, r'idea_categories', lookup="idea_category")
ideas_router.register(r'ideas', api_views.IdeaViewSet)

comments_router = routers.NestedSimpleRouter(ideas_router, r'ideas', lookup="idea")
comments_router.register(r'comments', api_views.IdeaCommentViewSet)

api_urlpatterns = [
    path("", include(router.urls)),
    path("", include(ideas_router.urls)),
    path("", include(comments_router.urls)),

]