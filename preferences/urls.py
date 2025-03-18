from django.urls import path
from .views import preferences, save_preferences, update_budget

urlpatterns = [
    path("", preferences, name="preferences"),  # Agrega esta línea
    path("save/", save_preferences, name="save_preferences"),
    path("update-budget/", update_budget, name="update_budget"),
]
