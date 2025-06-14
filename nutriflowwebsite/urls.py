"""
URL configuration for nutriflowwebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from meal import views as mealViews
from accounts import views as accountViews

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mealViews.home),
    path('signupaccount/', accountViews.signupaccount),
    path('preferences/', include('preferences.urls')),
    path('accounts/', include('accounts.urls')),
    path('loginaccount/', accountViews.loginaccount),
    path('accounts/', include('accounts.urls')),
    path('accounts/home/perfil/', accountViews.profile_view, name='perfil'),
    path('perfil/', accountViews.profile_view, name='perfil'),	
    path('supermarket/', include('supermarket.urls')),
    path('ia/', include('ia.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
