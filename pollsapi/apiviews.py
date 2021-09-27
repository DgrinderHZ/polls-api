from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ChoiceSerializer, QuestionSerializer, VoteSerializer

from pollsapp.models import Question, Choice


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer
