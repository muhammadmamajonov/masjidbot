from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = 'login'),
    path('chiqish/', views.chiqish, name = 'chiqish'),
]
# parol:Masjidbotadmin123