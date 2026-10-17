from django import forms
from .models import Empleado, ContratoLaboral, Cargo


class _EstiloMixin:
    """Agrega clases CSS y widgets de fecha a todos los campos."""

    def _estilizar(self):
        for nombre, campo in self.fields.items():
            if isinstance(campo, forms.DateField):
                campo.widget = forms.DateInput(
                    attrs={'class': 'campo', 'type': 'date'}, format='%Y-%m-%d')
            elif isinstance(campo.widget, forms.Select):
                campo.widget.attrs['class'] = 'campo-select'
            else:
                campo.widget.attrs['class'] = 'campo'


class EmpleadoForm(_EstiloMixin, forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'tipo_documento', 'numero_documento',
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'correo_electronico', 'telefono', 'fecha_ingreso', 'estado_empleado',
        ]
        labels = {
            'numero_documento': 'Número de documento',
            'correo_electronico': 'Correo electrónico',
            'estado_empleado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._estilizar()

    def clean_numero_documento(self):
        return self.cleaned_data['numero_documento'].strip()

    def clean_correo_electronico(self):
        # '' chocaría con el UNIQUE de MySQL; se guarda NULL cuando está vacío.
        return (self.cleaned_data.get('correo_electronico') or '').strip().lower() or None

    def clean_telefono(self):
        return (self.cleaned_data.get('telefono') or '').strip() or None


class _CargoChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.departamento.nombre} · {obj.nombre}'


class ContratoForm(_EstiloMixin, forms.ModelForm):
    cargo = _CargoChoiceField(queryset=Cargo.objects.none())

    class Meta:
        model = ContratoLaboral
        fields = ['cargo', 'tipo_contrato', 'fecha_inicio', 'fecha_fin',
                  'salario_base', 'estado_contrato']
        labels = {'salario_base': 'Salario base (COP)', 'estado_contrato': 'Estado'}

    def __init__(self, *args, empleado, **kwargs):
        super().__init__(*args, **kwargs)
        self.empleado = empleado
        self.fields['cargo'].queryset = (
            Cargo.objects.filter(activo=True).select_related('departamento'))
        self._estilizar()

    def clean(self):
        datos = super().clean()
        inicio, fin = datos.get('fecha_inicio'), datos.get('fecha_fin')
        if inicio and fin and fin < inicio:
            self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a la de inicio.')
        if datos.get('estado_contrato') == ContratoLaboral.Estado.VIGENTE:
            if self.empleado.contratos.filter(estado_contrato='VIGENTE').exists():
                self.add_error(
                    'estado_contrato',
                    'Este empleado ya tiene un contrato vigente. Finalízalo antes de crear otro.')
        return datos

    def save(self, commit=True):
        contrato = super().save(commit=False)
        contrato.empleado = self.empleado
        if commit:
            contrato.save()
        return contrato
