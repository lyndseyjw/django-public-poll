from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# for Djangos 'generic views' system
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     # render function takes request object as 1st arg, template name as 2nd arg, & dictionary as optional 3rd arg
#     # it returns an HttpResponse object of given template rendered with given context
#     return render(request, 'polls/index.html', context)

# Djangos 'generic views' system
# ListView generic view displays a list of objects
class IndexView(generic.ListView):
    # ListView by default uses template called <app name>/<model name>_list.html
    template_name = 'polls/index.html'
    # auto generated context variable = <model name>_list
    # use context_object_name attribute to override this
    # don't need to do in DetailView because by default, uses <model name>
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now(), 
        ).order_by('-pub_date')[:5]

# Django requires 2 things : either returning an HttpResponse object containing the content for the requested page OR raising an exception such as Http404
# def detail(request, question_id):
#     # this get_object_or_404 function takes Django model as 1st arg & arbitrary number of keyword args, which it passes to the get() function of the model's manager.. it raises Http404 if the object doesn't exist
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# Djangos 'generic views' system
# DetailView generic view displays a detail page for a particular type of object
class DetailView(generic.DetailView):
    # generic view needs to know what Model acting upon.. uses this 'model' attribute
    model = Question
    # by default, DetailView uses a template called <app name>/<model name>_detail.html
    # template_name attribute tells Django to use specific template name rather than auto-generated default one
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# Djangos 'generic views' system
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            # request.choice values are always strings
            # this request will raise KeyError if choice wasnt provided in POST data
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form with an error message if choice wasnt given
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # always return an HttpResponseRedirect after successfully dealing with POST data
            # this prevents data from being posted twice if a user hits the Back button
            # redircting is best practice after successfully dealing with POST data
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))