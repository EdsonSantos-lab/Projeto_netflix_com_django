from django.apps import AppConfig
import os


class FilmeConfig(AppConfig):
    name = "filme"

    def ready(self):
        from .models import Usuario

        email = os.getenv("EMAIL_ADMIN")
        senha = os.getenv("SENHA_ADMIN")

        if not email or not senha:
            return

        if not Usuario.objects.filter(email=email).exists():
            Usuario.objects.create_superuser(
                username="admin",
                email=email,
                password=senha,
                is_active=True,
                is_staff=True,
            )