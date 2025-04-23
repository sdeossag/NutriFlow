from django.db import models
from django.contrib.auth.models import User
from supermarket.models import Supermarket

class GeneratedDiet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    diet_text = models.TextField()  # Aquí se guarda la recomendación generada por OpenAI

    def __str__(self):
        return f"Dieta generada para {self.user.username} - {self.date_created}"

class DietProduct(models.Model):
    diet = models.ForeignKey(GeneratedDiet, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    quantity = models.FloatField()  # Cantidad recomendada del producto (por ejemplo, en gramos o unidades)

    def __str__(self):
        return f"{self.product.nombre_producto} ({self.quantity} unidades)"
