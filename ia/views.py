from django.shortcuts import render
from preferences.models import Preferences
from supermarket.models import Supermarket
import openai
import os
from dotenv import load_dotenv

# Cargar clave API
load_dotenv('C:/Users/ASUS/Downloads/NutriFlow-main/NutriFlow-main/openAI.env')
openai.api_key = os.getenv("OPEN_AI_API_KEY")
if not openai.api_key:
    raise ValueError("No se cargó la clave API de OpenAI correctamente.")

def generate_meal_plan(request):
    user = request.user
    prefs = Preferences.objects.filter(user=user).first()

    if not prefs:
        return render(request, 'meal_plan_result.html', {
            'error': 'No has configurado tus preferencias nutricionales.'
        })

    if request.method == 'POST':  # Aquí generamos el plan solo si se ha presionado el botón
        # Obtener todos los productos disponibles de la base de datos
        productos_disponibles = Supermarket.objects.all()

        # Crear la lista de productos con precios y macronutrientes
        productos_lista = ""
        for prod in productos_disponibles:
            productos_lista += (
                f"- {prod.nombre_producto} ({prod.marca_producto}): "
                f"{prod.calorias} kcal, {prod.proteinas}g proteínas, "
                f"{prod.carbohidratos}g carbohidratos, {prod.grasas}g grasas, "
                f"Precio: {prod.precio_producto}€, Supermercado: {prod.nombre_supermercado}\n"
            )

        # Ajustar el prompt para OpenAI
        prompt = f"""
        Eres un nutricionista experto en planes alimenticios.

        Crea un plan alimenticio para un día completo (desayuno, almuerzo, cena y 2 snacks) usando **exclusivamente** productos de la siguiente lista.

        Cada comida debe:
        - Incluir el nombre del producto y su marca exactamente como aparece
        - Indicar la cantidad usada (en gramos o mililitros)
        - Calcular y mostrar los macronutrientes por comida (calorías, proteínas, carbohidratos y grasas)
        - Usar una preparación sencilla

        🚫 No debes usar productos que no estén en la lista. No inventes productos ni nombres. Usa solo los listados aquí:

        {productos_lista}

        ⚠️ El total diario del plan debe cumplir los siguientes requerimientos nutricionales del usuario, con un margen de error máximo de ±5%:

        - Calorías: {prefs.calorias} kcal
        - Proteínas: {prefs.proteinas} g
        - Carbohidratos: {prefs.carbohidratos} g
        - Grasas: {prefs.grasas} g

        ❗ No subestimes los valores nutricionales. Ajusta las cantidades de los productos si es necesario para alcanzar los requerimientos.

        ✅ Al final del plan, incluye una sección con el título: **Macronutrientes totales del día**, que sume todos los valores de las comidas.

        ✅ Luego incluye una sección titulada: **Lista de Compras**, usando una tabla con las siguientes columnas:

        | Producto | Marca | Supermercado | Cantidad | Precio Total (€) |

        No incluyas ninguna explicación adicional. Todo debe estar en español.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "Eres un nutricionista que crea planes alimenticios solo con productos de supermercado específicos."},
                          {"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=1800
            )
            meal_plan_text = response['choices'][0]['message']['content']
        except Exception as e:
            return render(request, 'meal_plan_result.html', {'error': str(e)})

        return render(request, 'meal_plan_result.html', {
            'meal_plan': meal_plan_text,
        })

    return render(request, 'meal_plan_result.html')
