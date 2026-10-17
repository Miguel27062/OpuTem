
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Departamento,
    Cargo,
    Empleado,
    ContratoLaboral,
    NovedadLaboral,
)


@admin.register(Departamento)
class DepartamentoAdmin(ModelAdmin):
    list_display = (
        "id_departamento",
        "nombre",
        "activo",
        "fecha_creacion",
    )
    list_display_links = ("nombre",)
    search_fields = ("nombre", "descripcion")
    list_filter = ("activo",)
    ordering = ("nombre",)
    list_per_page = 20
    list_filter_submit = True


@admin.register(Cargo)
class CargoAdmin(ModelAdmin):
    list_display = (
        "id_cargo",
        "nombre",
        "departamento",
        "activo",
        "fecha_creacion",
    )
    list_display_links = ("nombre",)
    search_fields = (
        "nombre",
        "descripcion",
        "departamento__nombre",
    )
    list_filter = ("departamento", "activo")
    list_select_related = ("departamento",)
    ordering = ("departamento__nombre", "nombre")
    list_per_page = 20
    list_filter_submit = True


@admin.register(Empleado)
class EmpleadoAdmin(ModelAdmin):
    list_display = (
        "id_empleado",
        "numero_documento",
        "nombre_completo",
        "correo_electronico",
        "telefono",
        "fecha_ingreso",
        "estado_empleado",
    )
    list_display_links = ("numero_documento", "nombre_completo")
    search_fields = (
        "numero_documento",
        "primer_nombre",
        "segundo_nombre",
        "primer_apellido",
        "segundo_apellido",
        "correo_electronico",
    )
    list_filter = (
        "estado_empleado",
        "tipo_documento",
        "fecha_ingreso",
    )
    list_select_related = ()
    date_hierarchy = "fecha_ingreso"
    ordering = ("primer_apellido", "primer_nombre")
    list_per_page = 25
    list_filter_submit = True
    save_on_top = True

    readonly_fields = (
        "fecha_creacion",
        "fecha_actualizacion",
    )

    fieldsets = (
        (
            "Identificación",
            {
                "fields": (
                    "tipo_documento",
                    "numero_documento",
                )
            },
        ),
        (
            "Información personal",
            {
                "fields": (
                    "primer_nombre",
                    "segundo_nombre",
                    "primer_apellido",
                    "segundo_apellido",
                )
            },
        ),
        (
            "Contacto",
            {
                "fields": (
                    "correo_electronico",
                    "telefono",
                )
            },
        ),
        (
            "Información laboral",
            {
                "fields": (
                    "fecha_ingreso",
                    "estado_empleado",
                )
            },
        ),
        (
            "Auditoría",
            {
                "classes": ("collapse",),
                "fields": (
                    "fecha_creacion",
                    "fecha_actualizacion",
                ),
            },
        ),
    )


@admin.register(ContratoLaboral)
class ContratoLaboralAdmin(ModelAdmin):
    list_display = (
        "id_contrato",
        "empleado",
        "cargo",
        "tipo_contrato",
        "fecha_inicio",
        "fecha_fin",
        "salario_base",
        "estado_contrato",
    )
    list_display_links = ("empleado",)
    search_fields = (
        "empleado__numero_documento",
        "empleado__primer_nombre",
        "empleado__primer_apellido",
        "cargo__nombre",
    )
    list_filter = (
        "estado_contrato",
        "tipo_contrato",
        "fecha_inicio",
    )
    list_select_related = ("empleado", "cargo")
    date_hierarchy = "fecha_inicio"
    ordering = ("-fecha_inicio",)
    list_per_page = 25
    list_filter_submit = True
    save_on_top = True


@admin.register(NovedadLaboral)
class NovedadLaboralAdmin(ModelAdmin):
    list_display = (
        "id_novedad",
        "empleado",
        "tipo_novedad",
        "fecha_inicio",
        "fecha_fin",
        "estado_novedad",
        "fecha_creacion",
    )
    list_display_links = ("empleado",)
    search_fields = (
        "empleado__numero_documento",
        "empleado__primer_nombre",
        "empleado__primer_apellido",
        "descripcion",
    )
    list_filter = (
        "tipo_novedad",
        "estado_novedad",
        "fecha_inicio",
    )
    list_select_related = ("empleado",)
    date_hierarchy = "fecha_inicio"
    ordering = ("-fecha_inicio",)
    list_per_page = 25
    list_filter_submit = True
    save_on_top = True

    readonly_fields = (
        "fecha_creacion",
        "fecha_actualizacion",
    )
