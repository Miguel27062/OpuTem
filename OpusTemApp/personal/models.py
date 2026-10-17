
from django.db import models


class Departamento(models.Model):
    id_departamento = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        managed = False
        db_table = 'departamentos'
        ordering = ['nombre']
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    id_cargo = models.BigAutoField(primary_key=True)

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        db_column='id_departamento',
        related_name='cargos',
    )

    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        managed = False
        db_table = 'cargos'
        ordering = ['departamento__nombre', 'nombre']
        verbose_name = 'cargo'
        verbose_name_plural = 'cargos'

    def __str__(self):
        return f'{self.nombre} ({self.departamento.nombre})'


class Empleado(models.Model):

    class TipoDocumento(models.TextChoices):
        CC = 'CC', 'Cédula de ciudadanía'
        CE = 'CE', 'Cédula de extranjería'
        PASAPORTE = 'PASAPORTE', 'Pasaporte'
        OTRO = 'OTRO', 'Otro'

    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        INACTIVO = 'INACTIVO', 'Inactivo'
        RETIRADO = 'RETIRADO', 'Retirado'
        LICENCIA = 'LICENCIA', 'En licencia'

    id_empleado = models.BigAutoField(primary_key=True)

    tipo_documento = models.CharField(
        max_length=10,
        choices=TipoDocumento.choices,
        default=TipoDocumento.CC,
    )

    numero_documento = models.CharField(max_length=30)
    primer_nombre = models.CharField(max_length=80)
    segundo_nombre = models.CharField(
        max_length=80,
        blank=True,
        null=True,
    )
    primer_apellido = models.CharField(max_length=80)
    segundo_apellido = models.CharField(
        max_length=80,
        blank=True,
        null=True,
    )

    correo_electronico = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )

    telefono = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    fecha_ingreso = models.DateField()

    estado_empleado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ACTIVO,
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        managed = False
        db_table = 'empleados'
        unique_together = (
            ('tipo_documento', 'numero_documento'),
        )
        ordering = ['primer_apellido', 'primer_nombre']
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        partes = [
            self.primer_nombre,
            self.segundo_nombre,
            self.primer_apellido,
            self.segundo_apellido,
        ]

        return ' '.join(
            parte for parte in partes if parte
        )

    @property
    def contrato_vigente(self):
        # Aprovecha los contratos precargados por la vista.
        if hasattr(self, 'contratos_vigentes'):
            contratos = self.contratos_vigentes
            return contratos[0] if contratos else None

        # Si no fueron precargados, consulta la base de datos.
        return (
            self.contratos
            .filter(estado_contrato='VIGENTE')
            .select_related('cargo__departamento')
            .first()
        )


class ContratoLaboral(models.Model):

    class Tipo(models.TextChoices):
        INDEFINIDO = 'INDEFINIDO', 'Término indefinido'
        FIJO = 'FIJO', 'Término fijo'
        OBRA_LABOR = 'OBRA_LABOR', 'Obra o labor'
        APRENDIZAJE = 'APRENDIZAJE', 'Aprendizaje'
        PRESTACION_SERVICIOS = (
            'PRESTACION_SERVICIOS',
            'Prestación de servicios',
        )
        OTRO = 'OTRO', 'Otro'

    class Estado(models.TextChoices):
        VIGENTE = 'VIGENTE', 'Vigente'
        FINALIZADO = 'FINALIZADO', 'Finalizado'
        SUSPENDIDO = 'SUSPENDIDO', 'Suspendido'

    id_contrato = models.BigAutoField(primary_key=True)

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        db_column='id_empleado',
        related_name='contratos',
    )

    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        db_column='id_cargo',
        related_name='contratos',
    )

    tipo_contrato = models.CharField(
        max_length=25,
        choices=Tipo.choices,
    )

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(
        blank=True,
        null=True,
    )

    salario_base = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    estado_contrato = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.VIGENTE,
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        managed = False
        db_table = 'contratos_laborales'
        ordering = ['-fecha_inicio']
        verbose_name = 'contrato laboral'
        verbose_name_plural = 'contratos laborales'

    def __str__(self):
        return (
            f'{self.get_tipo_contrato_display()} · '
            f'{self.empleado}'
        )


class NovedadLaboral(models.Model):

    class Tipo(models.TextChoices):
        AUSENCIA = 'AUSENCIA', 'Ausencia'
        PERMISO = 'PERMISO', 'Permiso'
        VACACIONES = 'VACACIONES', 'Vacaciones'
        INCAPACIDAD = 'INCAPACIDAD', 'Incapacidad'
        HORAS_EXTRA = 'HORAS_EXTRA', 'Horas extra'
        BONIFICACION = 'BONIFICACION', 'Bonificación'
        OTRA = 'OTRA', 'Otra'

    class Estado(models.TextChoices):
        REGISTRADA = 'REGISTRADA', 'Registrada'
        APROBADA = 'APROBADA', 'Aprobada'
        RECHAZADA = 'RECHAZADA', 'Rechazada'
        PROCESADA = 'PROCESADA', 'Procesada'

    id_novedad = models.BigAutoField(primary_key=True)

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        db_column='id_empleado',
        related_name='novedades',
    )

    tipo_novedad = models.CharField(
        max_length=15,
        choices=Tipo.choices,
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField(
        blank=True,
        null=True,
    )

    descripcion = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    estado_novedad = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.REGISTRADA,
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        managed = False
        db_table = 'novedades_laborales'
        ordering = ['-fecha_inicio']
        verbose_name = 'novedad laboral'
        verbose_name_plural = 'novedades laborales'

    def __str__(self):
        return (
            f'{self.get_tipo_novedad_display()} · '
            f'{self.empleado}'
        )
