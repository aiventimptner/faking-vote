from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from .forms import DecisionForm, VoteForm
from .models import Decision, Option, Vote


class DecisionIndex(ListView):
    template_name = 'votes/index.html'

    def get_queryset(self):
        dt = timezone.now() - timedelta(minutes=5)
        pending_decisions = Decision.objects.filter(end__gt=dt).order_by('start').all()
        return pending_decisions


class DecisionCreate(LoginRequiredMixin, FormView):
    template_name = 'votes/decision/create.html'
    form_class = DecisionForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        for text in ["Dafür", "Dagegen", "Enthaltung"]:
            option = Option.objects.create(decision=form.instance, text=text)
            option.save()
        return super().form_valid(form)


class DecisionInfo(LoginRequiredMixin, DetailView):
    template_name = 'votes/decision/info.html'
    model = Decision
    form_class = VoteForm

    def get_context_data(self, **kwargs):
        decision = Decision.objects.get(pk=self.kwargs['pk'])
        votes = Vote.objects.filter(
            user=self.request.user,
            option__in=[option.id for option in decision.option_set.all()],
        ).all()

        voting_permitted = False
        if votes:
            message = "Du hast bereits an der Abstimmung teilgenommen!"
        elif timezone.now() < decision.start:
            message = "Die Abstimmung hat noch nicht begonnen!"
        elif timezone.now() > decision.end:
            message = "Die Abstimmung ist bereits zu Ende!"
        else:
            voting_permitted = True
            message = None

        context = super().get_context_data()
        context['status'] = {
            'voting_permitted': voting_permitted,
            'message': message,
        }
        return context


class VoteCreate(LoginRequiredMixin, FormView):
    template_name = 'votes/vote/create.html'
    form_class = VoteForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['decision'] = get_object_or_404(Decision, pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['decision_id'] = self.kwargs['pk']
        return kwargs

    def post(self, request, *args, **kwargs):
        decision = Decision.objects.get(pk=self.kwargs['pk'])
        votes = Vote.objects.filter(
            user=self.request.user,
            option__in=[option.id for option in decision.option_set.all()],
        ).all()
        if votes:
            return HttpResponseForbidden("User has already voted")
        elif timezone.now() < decision.start:
            return HttpResponseForbidden("Voting has not started yet")
        elif timezone.now() > decision.end:
            return HttpResponseForbidden("Vote is already finished")
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
