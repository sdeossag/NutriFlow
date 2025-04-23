from django.contrib import admin
from .models import GeneratedDiet, DietProduct  # Importar los modelos de la app ai

# Registra los modelos en el admin de Django
admin.site.register(GeneratedDiet)
admin.site.register(DietProduct)
