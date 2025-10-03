from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from .serializers import IdeaSerializer
from .models import Idea

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

def index(request):
    latest_ideas= Idea.objects.order_by("created_at")[:10]
    context = {"latest_ideas": latest_ideas}
    return render(request, "ideas/index.html", context)

def details(request, idea_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
    except Idea.DoesNotExist:
        raise Http404("Idea does not exist")
    return render(request, "ideas/details.html", {"idea": idea})
