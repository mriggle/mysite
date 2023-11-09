from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, Response
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Count



class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# class ResultsView(LoginRequiredMixin, generic.DetailView):
#     model = Question
#     template_name = "polls/results.html"
#     context_object_name = "votes_list"
#     def get_queryset(self):
#         return [1,2,3]
        # questionObj = get_object_or_404(Question)
        # # question = Question
        # # votes = Response.objects.filter(question__name=question).count()
        # return questionObj.choice_set
    

def results(request, question_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    question = get_object_or_404(Question, pk=question_id)

    list = Choice.objects.filter(question=question).annotate(votes=Count("response"))

    context = {"question": question, "list": list}
    return render(request, "polls/results.html", context)




def vote(request, question_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        r = Response(user=request.user, choice=selected_choice, date=timezone.now())
        r.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
