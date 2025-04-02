from django.shortcuts import render, redirect
from .models import Preferences  # Asegúrate de que tienes este modelo

def preferences_view(request):
    preferences = None
    if request.user.is_authenticated:
        preferences = Preferences.objects.filter(user=request.user).first()
    
    return render(request, 'preferences.html', {'preferences': preferences})

def save_preferences(request):
    if request.method == 'POST':
        preferences, created = Preferences.objects.get_or_create(user=request.user)
        preferences.genero = request.POST.get('genero')
        preferences.objetivo = request.POST.get('objetivo')
        preferences.edad = request.POST.get('edad')
        preferences.peso = request.POST.get('peso')
        preferences.altura = request.POST.get('altura')
        preferences.nivel_actividad = request.POST.get('nivel_actividad')
        preferences.presupuesto = request.POST.get('presupuesto')
        preferences.alergias = request.POST.get('alergias')
        preferences.save()
        return redirect('preferences')  # Redirige después de guardar
    return redirect('preferences')






