from rest_framework import routers
from django.urls import path
from ideas.views import IdeaViewSet

router = routers.DefaultRouter()
router.register(r'ideas', IdeaViewSet)

urlpatterns = router.urls
