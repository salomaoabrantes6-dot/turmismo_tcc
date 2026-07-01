from django.urls import path
from . import views

urlpatterns = [
    path('acess_area_admin/', views.login_view, name='login'),
    path('home', views.index, name='index'),
    path('', views.ladingPage, name='ladingPage')
]
