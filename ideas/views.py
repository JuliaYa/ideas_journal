from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from .serializers import IdeaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

@api_view(['GET'])
def idea_details(_, idea_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
    except Idea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = IdeaSerializer(idea)
    return Response(serializer.data)

@api_view(['POST'])
def create_idea(request):
    
    serializer = IdeaSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
