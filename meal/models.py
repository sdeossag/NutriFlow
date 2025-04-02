from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    
class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="meal_preferences")  # 👈 Diferencia este modelo
    dietary_restrictions = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
