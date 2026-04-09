from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .models import Idea, NoteEntry
from .serializers import IdeaSerializer, NoteEntrySerializer


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class NoteEntryViewSet(viewsets.ModelViewSet):
    serializer_class = NoteEntrySerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return NoteEntry.objects.filter(idea_id=self.kwargs['idea_pk'])

    def perform_create(self, serializer):
        serializer.save(idea_id=self.kwargs['idea_pk'])


def index(request):
    latest_ideas = Idea.objects.order_by('created_at')[:10]
    context = {'latest_ideas': latest_ideas}
    return render(request, 'ideas/index.html', context)


def details(request, idea_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
    except Idea.DoesNotExist:
        raise Http404('Idea does not exist')
    return render(request, 'ideas/details.html', {'idea': idea})
