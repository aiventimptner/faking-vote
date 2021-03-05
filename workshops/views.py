from datetime import date
from django.views.generic import ListView, CreateView, TemplateView

from .forms import ParticipantForm
from .models import Workshop


class WorkshopList(ListView):
    model = Workshop
    queryset = Workshop.objects.filter(date__gte=date.today())


class ParticipantCreate(CreateView):
    template_name = 'workshops/participant_form.html'
    form_class = ParticipantForm
    success_url = 'success/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['workshops'] = Workshop.objects.all()
        return context

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class ParticipantCreateSuccess(TemplateView):
    template_name = 'workshops/participant_form_success.html'
