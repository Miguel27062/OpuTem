from django.urls import path
from . import views

app_name = 'personal'

urlpatterns = [
    path('', views.EmpleadoListView.as_view(), name='empleado_list'),
    path('nuevo/', views.EmpleadoCreateView.as_view(), name='empleado_create'),
    path('<int:pk>/', views.EmpleadoDetailView.as_view(), name='empleado_detail'),
    path('<int:pk>/editar/', views.EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('<int:pk>/contrato/nuevo/', views.ContratoCreateView.as_view(), name='contrato_create'),
]
