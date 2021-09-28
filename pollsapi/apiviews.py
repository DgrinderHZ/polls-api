from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from pollsapi.models import Poll
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .serializers import ChoiceSerializer, PollSerializer,\
     QuestionSerializer, VoteSerializer, UserSerializer

from pollsapp.models import Question, Choice


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response(
                {"error": "Wrong Credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


# variant2: APIView subclasses
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


# variant3: generics.* subclasses
class QuestionChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        querset = Choice.objects.filter(question_id=self.kwargs['pk'])
        return querset
    serializer_class = ChoiceSerializer


# variant4: viewsets.ModelViewSet
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('You can not delet this poll.')
        return super().destroy(request, *args, **kwargs)
