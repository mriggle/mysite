from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, Response
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Count, Value, BooleanField
from django.db import models

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    unanswered = Question.objects.exclude(choice__response__user_id=request.user.id)
    answered = Question.objects.filter(choice__response__user_id=request.user.id).distinct()

    context = {"answered": answered, "unanswered": unanswered}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if not Response.objects.filter(user=request.user, choice__question_id=question_id).exists():
        return redirect('../vote')
    
    userChoice = Response.objects.filter(user=request.user, choice__question_id=question_id).choice

    question = get_object_or_404(Question, pk=question_id)
    list = Choice.objects.filter(question=question).annotate(
        votes=Count("response")
    )



    context = {"question": question, "list": list}
    return render(request, "polls/results.html", context)

def vote(request, question_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if Response.objects.filter(user=request.user, choice__question_id=question_id).exists():
        return redirect('../results')
    
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
