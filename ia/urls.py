from django.urls import path
from . import views

urlpatterns = [
    path('generate-diet/', views.generate_meal_plan, name='generate_diet'),
]
