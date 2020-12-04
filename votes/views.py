from django.views import generic

from .models import Decision


class IndexView(generic.ListView):
    template_name = 'votes/index.html'

    def get_queryset(self):
        return Decision.objects.order_by('created')


class DetailView(generic.DetailView):
    template_name = 'votes/detail.html'
    model = Decision
