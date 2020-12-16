from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from .forms import CreateDecisionForm
from .models import Decision, Option


class DecisionIndex(ListView):
    template_name = 'votes/index.html'

    def get_queryset(self):
        return Decision.objects.order_by('created')


class DecisionCreate(LoginRequiredMixin, FormView):
    template_name = 'votes/decision/create.html'
    form_class = CreateDecisionForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        for text in ["Dafür", "Dagegen", "Enthaltung"]:
            option = Option.objects.create(decision=form.instance, text=text)
            option.save()
        return super().form_valid(form)


class DecisionInfo(DetailView):
    template_name = 'votes/decision/info.html'
    model = Decision
