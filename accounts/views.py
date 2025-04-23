from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from preferences.models import Preferences  # ✅ Importar desde la app correcta


def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {
                    'form': UserCreationForm(),
                    'error': 'El nombre de usuario ya está en uso. Intenta con otro.'
                })
        else:
            return render(request, 'signupaccount.html', {
                'form': UserCreationForm(),
                'error': 'Las contraseñas no coinciden.'
            })


def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])

        if user is None:
            return render(request, 'loginaccount.html', {
                'form': AuthenticationForm(),
                'error': 'El usuario y la contraseña no coinciden.'
            })
        else:
            login(request, user)
            return redirect('home')


@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    preferences = Preferences.objects.filter(user=request.user).first()

    if not preferences:
        return render(request, 'account.html', {
            'no_preferences': True
        })

    # Aquí podrías usar valores reales de logs diarios si los tienes
    calorias_consumidas = 1200
    proteinas_consumidas = 60
    carbohidratos_consumidos = 150
    grasas_consumidas = 40

    def porcentaje(actual, objetivo):
        return min(round((actual / objetivo) * 100, 2), 100) if objetivo > 0 else 0

    context = {
        'no_preferences': False,
        'preferences': preferences,
        'calorias_consumidas': calorias_consumidas,
        'proteinas_consumidas': proteinas_consumidas,
        'carbohidratos_consumidos': carbohidratos_consumidos,
        'grasas_consumidas': grasas_consumidas,
        'porcentaje_calorias': porcentaje(calorias_consumidas, preferences.calorias),
        'porcentaje_proteinas': porcentaje(proteinas_consumidas, preferences.proteinas),
        'porcentaje_carbohidratos': porcentaje(carbohidratos_consumidos, preferences.carbohidratos),
        'porcentaje_grasas': porcentaje(grasas_consumidas, preferences.grasas),
    }

    return render(request, 'account.html', context)
