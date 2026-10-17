from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),  # login, logout, cambio de clave
    path('empleados/', include('personal.urls')),
    path('', RedirectView.as_view(pattern_name='personal:empleado_list', permanent=False)),
]
