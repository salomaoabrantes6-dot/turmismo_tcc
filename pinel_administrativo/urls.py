from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pontos_turisticos/', views.atrativos_turisticos, name='atrativos_turisticos'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path("praiasBelas/", views.praiasBelas, name="praiasBelas"),
    
    path('logout_view/', views.logout_view, name='logout_view'),
    
    path('deletar_ponto/deletar/<int:pk>/', views.deletar_ponto, name='deletar_ponto'),
    path('deletar_praia/deletar/<int:pk>/', views.deletar_praia, name='deletar_praia'),
    
    path('atrativos_turisticos/<str:pk>/', views.atrativos_turisticos, name='atrativos_turisticos_editar'),
    path('praiasBelas/<str:pk>/', views.praiasBelas, name='praiasBelas_editar'),
    
    path('moderacao/<int:id>/<str:acao>/', views.acao_depoimento, name='acao_depoimento'),
    
]
