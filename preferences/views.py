from django.shortcuts import render
from .models import Preferences
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


def preferences(request):
    preference = Preferences.objects.all()
    return render(request, 'preferences.html', {'preference': preference})
def signupaccount(request):
    return render(request, 'signupaccount.html', {'signupaccount': 'signupaccount'})


@csrf_exempt  # Evita problemas de CSRF en desarrollo
def save_preferences(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Convertir JSON a diccionario Python
            
            # Extraer los datos del JSON recibido
            title = data.get("title")
            goals = data.get("goals", [])
            diet = data.get("diet", "")
            allergies = data.get("allergies", [])
            budget = data.get("budget", 0.0)  # Nuevo campo para presupuesto

            # Crear una nueva instancia del modelo Preferences
            preference = Preferences.objects.create(
                title=title,
                diet=diet,
                goals=", ".join([f"{g['title']} - {g['description']} ({g['deadline']})" for g in goals]),
                allergies=", ".join(allergies),
                budget=budget  # Guardar presupuesto
            )

            preference.save()  # Guardar en la base de datos

            return JsonResponse({"message": "Preferences saved successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def update_budget(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            budget = data.get("budget", 0.0)  # Obtener el nuevo presupuesto
            
            # Buscar la primera preferencia en la base de datos (ajustar si hay múltiples usuarios)
            preference = Preferences.objects.first()
            if preference:
                preference.budget = budget
                preference.save()
                return JsonResponse({"message": "Budget updated successfully!"}, status=200)
            else:
                return JsonResponse({"error": "No preference found"}, status=404)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)