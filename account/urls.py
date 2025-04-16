from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # Nueva URL para cerrar sesión
    path('profile/', views.user_profile, name='profile'),
    path('registro/paso1/', views.registro_paso1, name='registro_paso1'),
    path('registro/paso2/', views.registro_paso2, name='registro_paso2'),
    path('registro/paso3/', views.registro_paso3, name='registro_paso3'),
    path('registro/paso4/', views.registro_paso4, name='registro_paso4'),
    path('registro/completado/', views.registro_completado, name='registro_completado'),
]