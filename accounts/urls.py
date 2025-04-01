from django.urls import path
from . import views
from meal import views as mealViews

urlpatterns = [
    path('signupaccount/', views.signupaccount, name='signupaccount'),
    path('home/', mealViews.home, name='home'),
    path('loginaccount/', views.loginaccount, name='loginaccount'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
]