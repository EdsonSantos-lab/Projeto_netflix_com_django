from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Filme, Usuario
from .forms import CriarContaForm, FormHome
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#def homepage(request):
#   return render(request, "homepage.html")

# em class do django
class HomePage(FormView):
    template_name = "homepage.html"
    form_class = FormHome

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            #rediciona para a homefilmes
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs) # rediciona para a homepage
    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email).exists()
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')



# url- vew- html
#def homefilmes(request):
#    context = {}
#    lista_filmes = Filme.objects.all()
#    context['lista_filmes'] = lista_filmes
#    return render(request, "homefilmes.html", context)

class HomeFilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme
    # object_list

class DetalhesFilmes(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilmes.html"
    model = Filme
    # object -> cada filme
    def get(self, request, *args, **kwargs):
        # descobrir qual filme o usuario esta assesando
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        request.user.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetalhesFilmes, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)
        context["filmes_relacionados"] = filmes_relacionados

        return context

class Pesquisa(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get("query")
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Sair(TemplateView):
    template_name = "sair.html"
    model = Filme

class EditarPerfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('filme:login')

