from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from pollsapp.models import Question


def polls_list(request):
    MAX_OBJECTS = 20
    polls = Question.objects.all()[:MAX_OBJECTS]
    data = {"results": list(
        polls.values("question_text", "created_by__username", "pub_date"))}
    return JsonResponse(data)


def polls_detail(request, pk):
    poll = get_object_or_404(Question, pk=pk)
    data = {"results": {
        "question_text": poll.question_text,
        "created_by": poll.created_by.username,
        "pub_date": poll.pub_date
    }}
    return JsonResponse(data)
