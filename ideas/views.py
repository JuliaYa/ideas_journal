from django.shortcuts import render
from django.http import Http404

from .models import Idea


def index(request):
    latest_ideas= Idea.objects.order_by("created_at")[:10]
    context = {"latest_ideas": latest_ideas}
    return render(request, "ideas/index.html", context)

def details(request, idea_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
    except Idea.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "ideas/details.html", {"idea": idea})
