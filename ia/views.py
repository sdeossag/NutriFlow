from django.shortcuts import render
from preferences.models import Preferences
from supermarket.models import Supermarket
import openai
import os
from dotenv import load_dotenv
import json
import re

# Cargar clave API
load_dotenv('C:/Users/ASUS/Downloads/NutriFlow-main/NutriFlow-main/openAI.env')
openai.api_key = os.getenv("openai_apikey")
if not openai.api_key:
    raise ValueError("No se cargó la clave API de OpenAI correctamente.")

def generate_meal_plan(request):
    user = request.user
    prefs = Preferences.objects.filter(user=user).first()

    if not prefs:
        return render(request, 'meal_plan_result.html', {
            'error': 'No has configurado tus preferencias nutricionales.'
        })

    if request.method == 'POST':
        productos_disponibles = Supermarket.objects.all()

        productos_lista = ""
        for prod in productos_disponibles:
            productos_lista += (
                f"- {prod.nombre_producto} ({prod.marca_producto}): "
                f"{prod.calorias} kcal, {prod.proteinas}g proteínas, "
                f"{prod.carbohidratos}g carbohidratos, {prod.grasas}g grasas, "
                f"Precio: {prod.precio_producto}€, Supermercado: {prod.nombre_supermercado}\n"
            )

        # Separar el bloque JSON del f-string para evitar errores de sintaxis
        prompt_intro = f"""
Eres un nutricionista experto en planes de alimentación económica y saludable.

Crea un plan de comidas para un día (desayuno, snack 1, almuerzo, snack 2, cena) usando únicamente los productos de la siguiente lista:

{productos_lista}

Cada comida debe:
- Elegir productos con mejor relación costo/nutrición
- No superar el presupuesto disponible: {prefs.presupuesto} €
- Indicar cantidad, preparación y macronutrientes

⚠️ El total diario del plan debe cumplir estas metas nutricionales con un margen máximo de ±5%:

El formato de salida debe ser estrictamente JSON con esta estructura exacta (sin explicaciones):
"""

        prompt_json = """
{
  "meals": [
    {
      "name": "Desayuno",
      "items": [
        {
          "producto": "...",
          "marca": "...",
          "cantidad": "..."
        }
      ],
      "preparacion": "...",
      "macronutrientes": {
        "calorias": ...,
        "proteinas": ...,
        "carbohidratos": ...,
        "grasas": ...
      }
    }
  ],
  "totals": {
    "calorias": ...,
    "proteinas": ...,
    "carbohidratos": ...,
    "grasas": ...
  },
  "shopping_list": [
    {
      "producto": "...",
      "marca": "...",
      "supermercado": "...",
      "cantidad": "...",
      "precio": ...
    }
  ],
  "presupuesto": {
    "total_usuario":  """ + str(prefs.presupuesto) + """,
    "total_usado": ...,
    "restante": ...
  }
}

📌 Importante:
- Sé estricto con los valores nutricionales. Ajusta las cantidades si es necesario.
- NO inventes productos. Usa solo los listados proporcionados
- NO excedas el presupuesto
- Redondea precios a 2 decimales
"""

        full_prompt = prompt_intro + prompt_json

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un nutricionista que crea planes alimenticios solo con productos reales y económicos."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )

            json_text = response['choices'][0]['message']['content'].strip()

            if not json_text:
                return render(request, 'meal_plan_result.html', {'error': 'La respuesta de OpenAI está vacía.'})

            match = re.search(r'({.*})', json_text, re.DOTALL)
            if match:
                json_text = match.group(1)
            else:
                return render(request, 'meal_plan_result.html', {
                    'error': f"La respuesta no contiene JSON reconocible:\n\n{json_text}"
                })

            json_text = json_text.replace('\\"', '"').replace("\\n", "").strip()

            try:
                meal_plan_data = json.loads(json_text)
            except json.JSONDecodeError as e:
                return render(request, 'meal_plan_result.html', {
                    'error': f"Error al decodificar JSON: {e}\n\nRespuesta:\n{json_text}"
                })

            if not meal_plan_data.get("meals") or not meal_plan_data.get("shopping_list"):
                return render(request, 'meal_plan_result.html', {
                    'error': "El plan generado no contiene datos completos. Intenta nuevamente."
                })

            # Cálculo visual del presupuesto
            total_usado = meal_plan_data["presupuesto"]["total_usado"]
            total_usuario = meal_plan_data["presupuesto"]["total_usuario"]
            porcentaje_usado = (total_usado / total_usuario) * 100

            if porcentaje_usado >= 80:
                color = "danger"
                mensaje = f"🚨 ¡Cuidado! Estás usando el {porcentaje_usado:.2f}% de tu presupuesto diario."
            elif porcentaje_usado >= 50:
                color = "warning"
                mensaje = f"⚠️ Atención: llevas usado el {porcentaje_usado:.2f}% de tu presupuesto."
            else:
                color = "success"
                mensaje = f"✅ Presupuesto bajo control: solo has usado el {porcentaje_usado:.2f}%."

            alerta_presupuesto = {
                "porcentaje": round(porcentaje_usado, 2),
                "color": color,
                "mensaje": mensaje
            }

        except Exception as e:
            return render(request, 'meal_plan_result.html', {'error': str(e)})

        return render(request, 'meal_plan_result.html', {
            'meal_plan_json': meal_plan_data,
            'alerta_presupuesto': alerta_presupuesto
        })

    return render(request, 'meal_plan_result.html')