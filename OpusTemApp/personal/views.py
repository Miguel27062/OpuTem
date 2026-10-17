from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from .forms import ContratoForm, EmpleadoForm
from .models import ContratoLaboral, Empleado


class EmpleadoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Empleado
    permission_required = 'personal.view_empleado'
    template_name = 'personal/empleado_list.html'
    context_object_name = 'empleados'
    paginate_by = 15

    def get_queryset(self):
        vigentes = Prefetch(
            'contratos',
            queryset=ContratoLaboral.objects.filter(estado_contrato='VIGENTE')
            .select_related('cargo__departamento'),
            to_attr='contratos_vigentes')
        qs = Empleado.objects.prefetch_related(vigentes)

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(primer_nombre__icontains=q) | Q(segundo_nombre__icontains=q) |
                Q(primer_apellido__icontains=q) | Q(segundo_apellido__icontains=q) |
                Q(numero_documento__icontains=q) | Q(correo_electronico__icontains=q))

        estado = self.request.GET.get('estado', '')
        if estado in Empleado.Estado.values:
            qs = qs.filter(estado_empleado=estado)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)
        ctx.update(
            q=self.request.GET.get('q', ''),
            estado=self.request.GET.get('estado', ''),
            estados=Empleado.Estado.choices,
            qs=params.urlencode(),
        )
        return ctx


class EmpleadoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Empleado
    permission_required = 'personal.view_empleado'
    template_name = 'personal/empleado_detail.html'
    context_object_name = 'empleado'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        emp = self.object
        ctx['contratos'] = emp.contratos.select_related('cargo__departamento')
        ctx['novedades'] = emp.novedades.all()[:10]
        return ctx


class EmpleadoCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                         SuccessMessageMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    permission_required = 'personal.add_empleado'
    template_name = 'personal/empleado_form.html'
    success_message = 'Empleado creado.'
    extra_context = {'titulo': 'Nuevo empleado'}

    def get_success_url(self):
        return reverse('personal:empleado_detail', args=[self.object.pk])


class EmpleadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                         SuccessMessageMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    permission_required = 'personal.change_empleado'
    template_name = 'personal/empleado_form.html'
    success_message = 'Cambios guardados.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar a {self.object.nombre_completo}'
        return ctx

    def get_success_url(self):
        return reverse('personal:empleado_detail', args=[self.object.pk])


class ContratoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ContratoLaboral
    form_class = ContratoForm
    permission_required = 'personal.add_contratolaboral'
    template_name = 'personal/contrato_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.empleado = get_object_or_404(Empleado, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['empleado'] = self.empleado
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['empleado'] = self.empleado
        ctx['titulo'] = f'Nuevo contrato para {self.empleado.nombre_completo}'
        return ctx

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Contrato registrado.')
        return redirect('personal:empleado_detail', pk=self.empleado.pk)
