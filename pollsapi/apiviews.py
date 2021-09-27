from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

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


class VoteCreate(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get('voted_by')
        data = {'choice': choice_pk, 'question': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            choice = get_object_or_404(Choice, pk=choice_pk)
            choice.tally += 1
            choice.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)


class QuestionChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        querset = Choice.objects.filter(question_id=self.kwargs['pk'])
        return querset
    serializer_class = ChoiceSerializer
