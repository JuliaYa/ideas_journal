from rest_framework import routers
from ideas.views import IdeaViewSet

router = routers.DefaultRouter()
router.register(r'ideas', IdeaViewSet)
router.register(r'ideas/<int:idea_id>', IdeaViewSet, basename='idea_details')    
router.register(r'ideas/create', IdeaViewSet, basename='create_idea')

urlpatterns = router.urls
