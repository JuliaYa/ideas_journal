from rest_framework import routers
from django.urls import path
from ideas.views import IdeaViewSet, create_idea

router = routers.DefaultRouter()
router.register(r'ideas', IdeaViewSet)
router.register(r'ideas/<int:idea_id>', IdeaViewSet, basename='idea_details')    
# router.register(r'ideas/create/', IdeaViewSet, basename='create_idea')

urlpatterns = [
    path('ideas/create/', create_idea, name='create-idea'),
] + router.urls
