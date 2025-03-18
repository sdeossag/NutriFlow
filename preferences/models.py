from django.db import models

class Preferences(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(null=True, blank=True)
    allergies = models.CharField(max_length=200)
    diet = models.CharField(max_length=200)
    goals = models.CharField(max_length=200)
    description = models.TextField()
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Nuevo campo

    objects = models.Manager() 

    def __str__(self):
        return str(self.title)
