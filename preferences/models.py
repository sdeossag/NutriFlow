from django.db import models
from django.contrib.auth.models import User

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    genero = models.CharField(max_length=10, choices=[("male", "Hombre"), ("female", "Mujer")], null=True, blank=True)
    objetivo = models.CharField(max_length=20,null=True, blank=True, choices=[
        ("lose_weight", "Bajar de peso"),
        ("improve_health", "Mejorar salud"),
        ("gain_weight", "Subir de peso"),
    ])
    edad = models.IntegerField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    nivel_actividad = models.CharField(null=True, blank=True, max_length=15, choices=[
        ("sedentario", "Sedentario"),
        ("ligero", "Ligero"),
        ("moderado", "Moderado"),
        ("activo", "Activo"),
        ("muy_activo", "Muy Activo"),
    ])
    presupuesto = models.FloatField(null=True, blank=True)
    alergias = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Preferencias de {self.user.username}"
