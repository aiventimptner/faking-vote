from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from .forms import DecisionForm, VoteForm
from .models import Decision, Option


class DecisionCreate(LoginRequiredMixin, FormView):
    template_name = 'votes/create.html'
    form_class = DecisionForm
    success_url = reverse_lazy('votes:decisions')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        for text in ["Dafür", "Dagegen", "Enthaltung"]:
            option = Option.objects.create(decision=form.instance, text=text)
            option.save()
        return super().form_valid(form)


class DecisionInfo(LoginRequiredMixin, DetailView):
    template_name = 'votes/info.html'
    model = Decision
    form_class = VoteForm


class Decisions(LoginRequiredMixin, ListView):
    model = Decision
    template_name = 'votes/list.html'

    def get_queryset(self):
        decisions = Decision.objects.filter(
            voters__in=[self.request.user],
            end__gt=timezone.now(),
        ).exclude(
            options__votes__user=self.request.user,
        ).order_by('start')
        return decisions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Offene Abstimmungen"
        return context


class DecisionsOwned(LoginRequiredMixin, ListView):
    model = Decision
    template_name = 'votes/list.html'

    def get_queryset(self):
        return Decision.objects.filter(author=self.request.user).order_by('-end')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eigene Abstimmungen"
        return context


class Results(LoginRequiredMixin, ListView):
    model = Decision
    template_name = 'votes/list.html'
    queryset = Decision.objects.filter(end__lt=timezone.now()).order_by('-end')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Abgeschlossene Abstimmungen"
        return context


class ResultInfo(LoginRequiredMixin, DetailView):
    template_name = 'votes/info.html'
    model = Decision

    def get(self, request, *args, **kwargs):
        decision = get_object_or_404(Decision, pk=self.kwargs['pk'])
        if decision.state()['code'] != 'closed':
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


class VoteCreate(LoginRequiredMixin, FormView):
    template_name = 'votes/vote.html'
    form_class = VoteForm
    success_url = reverse_lazy('votes:decisions')

    def get_context_data(self, **kwargs):
        decision = get_object_or_404(Decision, pk=self.kwargs['pk'])

        context = super().get_context_data(**kwargs)
        context['decision'] = decision
        context['entitled_to_vote'] = self.request.user in decision.voters.all()
        context['user_has_voted'] = self.request.user not in decision.pending_voters()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['decision'] = Decision.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def post(self, request, *args, **kwargs):
        decision = Decision.objects.get(pk=self.kwargs['pk'])

        if decision.state()['code'] != 'open':
            # voting not allowed
            raise PermissionDenied()

        if self.request.user not in decision.voters.all():
            # user not entitled to vote
            raise PermissionDenied()

        if self.request.user not in decision.pending_voters():
            # user already voted
            raise PermissionDenied()

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
