from django.urls import path
from . import views

urlpatterns = [
    path('generate_diet/', views.generate_diet, name='generate_diet'),

]
