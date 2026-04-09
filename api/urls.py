from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from ideas.views import IdeaViewSet, NoteEntryViewSet

router = routers.DefaultRouter()
router.register(r'ideas', IdeaViewSet)

ideas_router = nested_routers.NestedDefaultRouter(router, r'ideas', lookup='idea')
ideas_router.register(r'notes', NoteEntryViewSet, basename='idea-notes')

urlpatterns = router.urls + ideas_router.urls
