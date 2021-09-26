from django.http.response import HttpResponseRedirect
from pollsapp.models import Choice, Question
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone as tz


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


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        ctx = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', ctx)
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(
            reverse('polls:results', args=(question_id,)))
