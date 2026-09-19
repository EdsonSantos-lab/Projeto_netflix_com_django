from django.urls import path, reverse_lazy
from .views import HomeFilmes, HomePage, DetalhesFilmes, Pesquisa, Sair, EditarPerfil, Criarconta
from django.contrib.auth import views as auth_views

# url , view , template
app_name = 'filme'

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path("filmes/", HomeFilmes.as_view(), name='homefilmes'),
    path("filmes/<int:pk>", DetalhesFilmes.as_view(), name='detalhesfilmes'),
    path("pesquisa/", Pesquisa.as_view(), name='pesquisa'),
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("sair/", Sair.as_view(), name='sair'),
    path("editarperfil/<int:pk>", EditarPerfil.as_view(), name='editarperfil'),
    path("criarconta/", Criarconta.as_view(), name='criarconta'),
    path("mudarsenha/", auth_views.PasswordChangeView.as_view(template_name='editarperfil.html',
                                                              success_url=reverse_lazy('filme:homefilmes')), name="mudarsenha"),
]
