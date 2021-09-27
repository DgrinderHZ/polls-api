from django.http.response import HttpResponseRedirect
from pollsapp.models import Choice, Question, Vote
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone as tz
from django.contrib.auth import get_user_model


User = get_user_model()

class IndexListView(generic.ListView):
    template_name = 'polls/index.html'
    # Overide the name (default: question_list)
    context_object_name = 'latest_question_list'

    # Overide to perform the order_by
    def get_queryset(self):
        """Return the last five published questions.
           Except those set for future publication.
        """
        return Question.objects.filter(
            pub_date__lte=tz.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=tz.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=tz.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        ctx = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', ctx)
    else:
        selected_choice.tally += 1
        selected_choice.save()
        # Create the vote
        vote = Vote()
        vote.question = question
        vote.choice = selected_choice
        vote.voted_by = request.user

        return HttpResponseRedirect(
            reverse('polls:results', args=(question_id,)))
