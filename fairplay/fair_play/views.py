from django.shortcuts import render
from .forms import PlayerCreationForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Player

# Create your views here.
def index(request):
    #Main page view
    return render(request, 'index.html')


class CreatePlayerView(CreateView):
    form_class = PlayerCreationForm
    template_name = 'playeradd.html'
    success_url = reverse_lazy('playerslist')

    def form_valid(self, form):
        messages.success(self.request, 'Player added successfully')
        return super().form_valid(form)


class PlayerListView(ListView):
    model = Player
    template_name = 'playerslist.html'
    context_object_name = 'players'
