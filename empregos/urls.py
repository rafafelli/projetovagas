from django.urls import path
from . import views

app_name = 'empregos'
urlpatterns = [
    path('', views.home, name='home'),
    path('contas/login/', views.login_view, name='login'),
    path('contas/logout/', views.logout_view, name='logout'),
    path('contas/registro/', views.registro_view, name='registro'),
    path('vagas/', views.vagas_view, name='vagas'),
    path('vagas/criar', views.criar_vaga, name='criar_vaga'),
    path('vagas/deletar/<int:vaga_id>/', views.deletar_vaga, name='deletar_vaga'),
    path('editar_vaga/<int:vaga_id>/', views.editar_vaga, name='editar_vaga'),
    path('vagas/ver', views.ver_vagas, name='ver_vagas'),
    path('vagas/filtrar', views.filtrar_vagas, name='filtrar_vagas'),
    path('aplicar_vaga/<int:vaga_id>', views.aplicar_vaga, name='aplicar_vaga'),
    path('cancelar_aplicacao/<int:vaga_id>', views.cancelar_aplicacao, name='cancelar_aplicacao'),
    path('vagas_aplicadas/', views.vagas_aplicadas, name='vagas_aplicadas'),
    path('relatorio/', views.relatorio, name='relatorio'),
]
