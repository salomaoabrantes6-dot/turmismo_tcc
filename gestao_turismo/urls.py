from django.urls import path
from . import views

urlpatterns = [
    path('', views.dash_board, name='dash_board'),
    path('pontos_turisticos/', views.pontos_turisticos, name='pontos_turisticos'),
    path("praiasBelas/", views.praiasBelas, name="praias"),
    
    path('logout_view/', views.logout_view, name='logout_view'),
    
    path('deletar_ponto/deletar/<int:pk>/', views.deletar_ponto, name='deletar_ponto'),
    path('deletar_praia/deletar/<int:pk>/', views.deletar_praia, name='deletar_praia'),
    
    path('pontos_turisticos/<str:pk>/', views.pontos_turisticos, name='pontos_turisticos_editar'),
    path('praiasBelas/<str:pk>/', views.praiasBelas, name='praiasBelas_editar'),
    
    path('moderacao/<int:id>/<str:acao>/', views.acao_depoimento, name='acao_depoimento'),
    
]
