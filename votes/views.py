from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from .forms import DecisionForm, VoteForm
from .models import Decision, Option, Vote


class DecisionCreate(LoginRequiredMixin, FormView):
    template_name = 'votes/decision/create.html'
    form_class = DecisionForm
    success_url = reverse_lazy('votes:decisions')

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


class Decisions(LoginRequiredMixin, ListView):
    model = Decision
    template_name = 'votes/decision/list.html'

    def get_queryset(self):
        return Decision.objects.filter(
            Q(voters__in=[self.request.user]),
            end__gt=timezone.now(),
        ).order_by('start')


class DecisionsOwned(LoginRequiredMixin, ListView):
    model = Decision
    template_name = 'votes/decision/owned.html'

    def get_queryset(self):
        return Decision.objects.filter(author=self.request.user)


class DecisionResults(LoginRequiredMixin, ListView):
    model = Decision
    template_name = 'votes/decision/results.html'

    def get_queryset(self):
        return Decision.objects.filter(end__lt=timezone.now()).order_by('-end').all()


class DecisionResult(LoginRequiredMixin, DetailView):
    template_name = 'votes/decision/result.html'
    model = Decision

    def get(self, request, *args, **kwargs):
        decision = get_object_or_404(Decision, pk=self.kwargs['pk'])
        if decision.state() != 'closed':
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


class VoteCreate(LoginRequiredMixin, FormView):
    template_name = 'votes/vote/create.html'
    form_class = VoteForm
    success_url = reverse_lazy('votes:decisions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['decision'] = get_object_or_404(Decision, pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['decision_id'] = self.kwargs['pk']
        return kwargs

    def get(self, request, *args, **kwargs):
        decision = get_object_or_404(Decision, pk=self.kwargs['pk'])

        if decision.state() != 'open':
            raise PermissionDenied()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        decision = Decision.objects.get(pk=self.kwargs['pk'])
        votes = Vote.objects.filter(
            user=self.request.user,
            option__in=[option.id for option in decision.options.all()],
        ).all()

        if decision.state() != 'open':
            raise PermissionDenied()

        if votes:
            raise PermissionDenied()

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
