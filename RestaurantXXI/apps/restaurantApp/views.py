from django.shortcuts import render
from time import time
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView,DetailView
from django.urls import reverse_lazy
from apps.usuario.mixins import LoginYSuperStaffMixin, ValidarPermisosMixin,LoginMixin,LoginMixin
from apps.usuario.models import Usuario
from apps.restaurantApp.models import Mesa, Inventario, Solicitud, Reserva, Receta
from apps.restaurantApp.forms import MesaForm,InventarioForm, SolicitudForm, RecetaForm, ReservaForm
from apps.restaurantApp.carrito import Carrito

# Vista para el model MESA

class InicioMesa(LoginYSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    template_name = 'restaurantApp/Mesa/listar_mesa.html'
    permission_required = ('restaurantApp.view_mesa', 'restaurantApp.add_mesa',
                           'restaurantApp.delete_mesa', 'restaurantApp.change_mesa')

class CrearMesa(LoginYSuperStaffMixin, ValidarPermisosMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'restaurantApp/Mesa/crear_mesa.html'
    permission_required = ('restaurantApp.view_mesa', 'restaurantApp.add_mesa',
                           'restaurantApp.delete_mesa', 'restaurantApp.change_mesa')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('restaurant:inicio_mesa')

class ListadoMesa(LoginYSuperStaffMixin, ValidarPermisosMixin, ListView):
    model = Mesa
    permission_required = ('restaurantApp.view_mesa', 'restaurantApp.add_mesa',
                           'restaurantApp.delete_mesa', 'restaurantApp.change_mesa')

    def get_queryset(self):
        return self.model.objects.filter(disponible = True)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('restaurant:inicio_mesa')

class ActualizarMesa(LoginYSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'restaurantApp/mesa/mesa.html'
    permission_required = ('restaurantApp.view_mesa', 'restaurantApp.add_mesa',
                           'restaurantApp.delete_mesa', 'restaurantApp.change_mesa')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES,instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('restaurant:inicio_mesa')

class EliminarMesa(LoginYSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    model = Mesa
    template_name = 'restaurantApp/Mesa/eliminar_mesa.html'
    permission_required = ('restaurantApp.view_mesa', 'restaurantApp.add_mesa',
                           'restaurantApp.delete_mesa', 'restaurantApp.change_mesa')

    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            mesa = self.get_object()
            mesa.disponible = False
            mesa.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('restaurant:listar_mesa')

# Vista para el model Inventarios

class InicioInventario(LoginMixin, ValidarPermisosMixin, TemplateView):
    template_name = 'restaurantApp/inventario/listar_inventario.html'
    permission_required = ('restaurantApp.view_inventario', 'restaurantApp.add_inventario',
                           'restaurantApp.delete_inventario', 'restaurantApp.change_inventario')

class CrearInventario(LoginMixin, ValidarPermisosMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'restaurantApp/inventario/crear_inventario.html'
    permission_required = ('restaurantApp.view_inventario', 'restaurantApp.add_inventario',
                           'restaurantApp.delete_inventario', 'restaurantApp.change_inventario')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('restaurant:inicio_inventario')

class ListadoInventario(LoginMixin, ValidarPermisosMixin, ListView):
    model = Inventario
    permission_required = ('restaurantApp.view_inventario', 'restaurantApp.add_inventario',
                           'restaurantApp.delete_inventario', 'restaurantApp.change_inventario')

    def get_queryset(self):
        return self.model.objects.filter(disponibilidad_stock = True)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('restaurant:inicio_inventario')

class ActualizarInventario(LoginMixin, ValidarPermisosMixin, UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'restaurantApp/inventario/inventario.html'
    permission_required = ('restaurantApp.view_inventario', 'restaurantApp.add_inventario',
                           'restaurantApp.delete_inventario', 'restaurantApp.change_inventario')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES,instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('restaurant:inicio_inventario')

class EliminarInventario(LoginMixin, ValidarPermisosMixin, DeleteView):
    model = Inventario
    template_name = 'restaurantApp/inventario/eliminar_inventario.html'
    permission_required = ('restaurantApp.view_inventario', 'restaurantApp.add_inventario',
                           'restaurantApp.delete_inventario', 'restaurantApp.change_inventario')

    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            inventario = self.get_object()
            inventario.disponibilidad_stock = False
            inventario.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('restaurant:listar_inventario')

#Vista para el modelos Solicitud
class InicioSolicitud(LoginMixin,ValidarPermisosMixin, TemplateView):
    template_name = 'restaurantApp/Solicitud/listar_solicitud.html'
    permission_required = ('restaurantApp.view_solicitud', 'restaurantApp.add_solicitud',
                           'restaurantApp.delete_solicitud', 'restaurantApp.change_solicitud')

class CrearSolicitud(LoginMixin, ValidarPermisosMixin, CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'restaurantApp/Solicitud/crear_solicitud.html'
    permission_required = ('restaurantApp.view_solicitud', 'restaurantApp.add_solicitud',
                           'restaurantApp.delete_solicitud', 'restaurantApp.change_solicitud')
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('restaurant:inicio_solicitud')

class ListadoSolicitud(LoginMixin, ValidarPermisosMixin, ListView):
    model = Solicitud
    permission_required = ('restaurantApp.view_solicitud', 'restaurantApp.add_solicitud',
                           'restaurantApp.delete_solicitud', 'restaurantApp.change_solicitud')
    def get_queryset(self):
        return self.model.objects.filter(estado = True)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('restaurant:inicio_solicitud')

class ActualizarSolicitud(LoginMixin, ValidarPermisosMixin, UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'restaurantApp/Solicitud/solicitud.html'
    permission_required = ('restaurantApp.view_solicitud', 'restaurantApp.add_solicitud',
                           'restaurantApp.delete_solicitud', 'restaurantApp.change_solicitud')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES,instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('restaurant:inicio_solicitud')

class EliminarSolicitud(LoginMixin, ValidarPermisosMixin, DeleteView):
    model = Solicitud
    template_name = 'restaurantApp/Solicitud/eliminar_solicitud.html'
    permission_required = ('restaurantApp.view_solicitud', 'restaurantApp.add_solicitud',
                           'restaurantApp.delete_solicitud', 'restaurantApp.change_solicitud')

    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            solicitud = self.get_object()
            solicitud.estado = False
            solicitud.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('restaurant:listado_solicitud')

#Vista Reserva

class InicioReserva(LoginMixin, ValidarPermisosMixin, TemplateView):
    template_name = 'restaurantApp/reserva/listar_reserva.html'
    permission_required = ('restaurantApp.view_reserva', 'restaurantApp.add_reserva',
                           'restaurantApp.delete_reserva', 'restaurantApp.change_reserva')

class RegistrarReserva(LoginMixin, ValidarPermisosMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'restaurantApp/reserva/registrar_reserva.html'
    permission_required = ('restaurantApp.view_reserva', 'restaurantApp.add_reserva',
                           'restaurantApp.delete_reserva', 'restaurantApp.change_reserva')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'La {self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('restaurant:inicio_reserva')

class ListadoReserva(LoginMixin, ValidarPermisosMixin, ListView):
    model = Reserva
    permission_required = ('restaurantApp.view_reserva', 'restaurantApp.add_reserva',
                           'restaurantApp.delete_reserva', 'restaurantApp.change_reserva')

    def get_queryset(self):
        return self.model.objects.filter(estado = True)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('restaurant:inicio_reserva')


class ActualizarReserva(LoginMixin, ValidarPermisosMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'restaurantApp/reserva/reserva.html'
    permission_required = ('restaurantApp.view_reserva', 'restaurantApp.add_reserva',
                           'restaurantApp.delete_reserva', 'restaurantApp.change_reserva')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('restaurant:inicio_reserva')

class EliminarReserva(LoginMixin, ValidarPermisosMixin, DeleteView):
    model = Reserva
    template_name = 'restaurantApp/reserva/eliminar_reserva.html'
    permission_required = ('restaurantApp.view_reserva', 'restaurantApp.add_reserva',
                           'restaurantApp.delete_reserva', 'restaurantApp.change_reserva')

    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            reserva = self.get_object()
            reserva.estado = False
            reserva.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('restaurant:listar_reserva')


#Vista receta

class InicioReceta(LoginMixin, ValidarPermisosMixin, TemplateView):
    template_name = 'restaurantApp/receta/listar_receta.html'
    permission_required = ('restaurantApp.view_receta', 'restaurantApp.add_receta',
                           'restaurantApp.delete_receta', 'restaurantApp.change_receta')

class CrearReceta(LoginMixin, ValidarPermisosMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'restaurantApp/receta/crear_receta.html'
    permission_required = ('restaurantApp.view_receta', 'restaurantApp.add_receta',
                           'restaurantApp.delete_receta', 'restaurantApp.change_receta')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'La {self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('restaurant:inicio_receta')

class ListadoReceta(LoginMixin,ValidarPermisosMixin,ListView):
    model = Receta
    permission_required = ('restaurantApp.view_receta', 'restaurantApp.add_receta',
                           'restaurantApp.delete_receta', 'restaurantApp.change_receta')

    def get_queryset(self):
        return self.model.objects.filter(disponible = True)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json' )
        else:
            return redirect('restaurant:inicio_receta')





class ActualizarReceta(LoginMixin, ValidarPermisosMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'restaurantApp/receta/receta.html'
    permission_required = ('restaurantApp.view_receta', 'restaurantApp.add_receta',
                           'restaurantApp.delete_receta', 'restaurantApp.change_receta')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('restaurant:inicio_receta')

class EliminarReceta(LoginMixin, ValidarPermisosMixin, DeleteView):
    model = Receta
    template_name = 'restaurantApp/receta/eliminar_receta.html'
    permission_required = ('restaurantApp.view_receta', 'restaurantApp.add_receta',
                           'restaurantApp.delete_receta', 'restaurantApp.change_receta')

    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            receta = self.get_object()
            receta.disponible = False
            receta.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('restaurant:listar_receta')


class ListadoRecetasDisponibles(LoginMixin,ListView):
    model = Receta
    paginate_by = 6
    template_name = 'restaurantApp/receta/receta_disponibles.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(disponible = True)
        return queryset

class DetalleRecetaDiponible(LoginMixin,DetailView):
    model = Receta
    template_name = 'restaurantApp/receta/detalle_recetas_disponible.html'

def boleta(request):
    return render(request,'boleta.html')




# Carrito

def tienda(request):
    receta = Receta.objects.all()
    return render(request, 'restaurant:listado_receta_disponibles', {'receta':receta})


def agregar_producto(request, receta_id):
    carrito = Carrito(request)
    receta = Receta.objects.get(id=receta_id)
    carrito.agregar(receta)
    return redirect('restaurant:listado_receta_disponibles')


def eliminar_producto(request, receta_id):
    carrito = Carrito(request)
    receta = Receta.objects.get(id=receta_id)
    carrito.eliminar(receta)
    return redirect('restaurant:listado_receta_disponibles')


def restar_producto(request, receta_id):
    carrito = Carrito(request)
    receta = Receta.objects.get(id=receta_id)
    carrito.restar(receta)
    return redirect('restaurant:listado_receta_disponibles')


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('restaurant:listado_receta_disponibles')


def guardar_carrito(request):
    carrito = Carrito(request)
    carrito.guardar_carrito()
    return redirect('restaurant:listado_receta_disponibles')
