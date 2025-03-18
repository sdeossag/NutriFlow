from django.db import models

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