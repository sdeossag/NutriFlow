from django.urls import path
from . import views

urlpatterns = [
    path('', views.preferences_view, name='preferences'),
    path('save-preferences/', views.save_preferences, name='save_preferences'),
]
