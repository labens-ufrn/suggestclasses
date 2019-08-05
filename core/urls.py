from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('<int:horario_id>/', views.detail, name='detail'),
]
