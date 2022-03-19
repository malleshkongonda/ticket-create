from django.core.exceptions import PermissionDenied
from django.urls import reverse
from vanilla import ListView, UpdateView, CreateView

from tickets.forms import TicketForm
from tickets.models import Ticket


class TicketListView(ListView):
    model = Ticket
    queryset = Ticket.objects.filter(public=True)


class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tickets:list')


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.public and request.user != self.object.created_by:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('tickets:list')
