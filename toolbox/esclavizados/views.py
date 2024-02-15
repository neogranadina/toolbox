from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.db import transaction, models
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from dal import autocomplete

from .models import (Lugar, PlaceHistorical, PersonaEsclavizada, PersonaNoEsclavizada, Documento, 
                     Archivo, Calidades, Hispanizaciones, Etonimos, Actividades,
                     PersonaLugarRel, Persona, PersonaRelaciones)

from .forms import (LugarForm, LugarHistoria, DocumentoForm, ArchivoForm, PersonaEsclavizadaForm,
                    CalidadesForm, HispanizacionesForm, EtnonimosForm, OcupacionesForm,
                    PersonaLugarRelForm, PersonaRelacionesForm)

# Create your views here.

def home(request):
    return render(request, 'esclavizados/home.html')

class LugarAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Lugar.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
            
        return qs

class PersonaEsclavizadaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = PersonaEsclavizada.objects.all()
        if self.q:
            qs = qs.filter(nombre_normalizado__icontains=self.q)
        return qs

class PersonaNoEsclavizadaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = PersonaNoEsclavizada.objects.all()
        if self.q:
            qs = qs.filter(nombre_normalizado__icontains=self.q)
        return qs
    
class LugarEventoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Lugar.objects.all()
        if self.q:
            qs = qs.filter(nombre_lugar__icontains=self.q)
        return qs
    

class DocumentoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Documento.objects.all()
        if self.q:
            qs = qs.filter(titulo__icontains=self.q)
        return qs


class ArchivoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Archivo.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs
    
class CalidadesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Calidades.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs

class HispanizacionesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Hispanizaciones.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs

class EtnonimosAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Etonimos.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs

class OcupacionesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Actividades.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs

# Create Views

class ArchivoCreateView(CreateView):
    model = Archivo
    form_class = ArchivoForm
    template_name = 'esclavizados/Add/archivo.html'
    success_url = reverse_lazy('archivo-browser')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_archivo'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/archivo_form_only.html']
        return ['esclavizados/Add/archivo.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'archivo_id': self.object.archivo_id,
                'archivo_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('archivo-detail', kwargs={'pk': self.object.pk})
        

class DocumentoCreateView(CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'esclavizados/Add/documento.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_documento'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        # Use a different template when the request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/documento_form_only.html']
        return ['esclavizados/Add/documento.html']
    
    def get_template_names(self):
        # Use a different template when the request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/documento_form_only.html']
        return ['esclavizados/Add/documento.html']
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.object = form.save()

        # Check if the request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return a JsonResponse with Documento data
            data = {
                'documento_id': self.object.documento_id,
                'documento_name': str(self.object)  # Adjust the name as per your model's __str__ method
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)
    
    def get_success_url(self):
        archivo_initial = self.request.GET.get('archivo_initial')
        if archivo_initial:
            return reverse('archivo-detail', kwargs={
                'pk': archivo_initial
            })
        else:
            return reverse_lazy('documento-detail', kwargs={'pk': self.object.pk})

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        
        archivo_initial = self.request.GET.get('archivo_initial')
        if archivo_initial:
            initial['archivo'] = archivo_initial
            
        return initial


class LugarCreateView(CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'esclavizados/Add/lugar.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_lugar'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/lugar.html']
        return ['esclavizados/Add/lugar.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'lugar_id': self.object.lugar_id,
                'lugar_name': str(self.object)  
            }
            return JsonResponse(data)

        return super().form_valid(form)
    
    def get_success_url(self):
        #return reverse_lazy('lugar-detail', kwargs={'pk': self.object.pk})
        return reverse_lazy('home')
    

class PersonaEsclavizadaCreateView(CreateView):
    model = PersonaEsclavizada
    form_class = PersonaEsclavizadaForm
    template_name = 'esclavizados/Add/peresclavizada.html'
    success_url = reverse_lazy('personasesclavizadas-browse')
    
    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        else:
            return reverse('documento-browse')
    
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            initial['documentos'] = documento_initial
        
        return initial


# create views for RElations

class PersonaEsclavizadaLugarRelCreateView(CreateView):
    model = PersonaLugarRel
    form_class = PersonaLugarRelForm
    template_name = 'esclavizados/Relaciones/personaesclavizada_x_lugar.html'
    success_url = reverse_lazy('documento-browse')

    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        else:
            return reverse('documento-browse')

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        
        documento_initial = self.request.GET.get('documento_initial')
        personaesclavizada_initial = self.request.GET.get('personaesclavizada_initial')
        if documento_initial:
            initial['documento'] = documento_initial
        if personaesclavizada_initial:
            initial['persona'] = personaesclavizada_initial
        return initial

class PersonaPersonaRelCreateView(CreateView):
    model = PersonaRelaciones
    form_class = PersonaRelacionesForm
    template_name = 'esclavizados/Relaciones/persona_x_persona.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        else:
            return reverse('documento-browse')
        
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        
        documento_initial = self.request.GET.get('documento_initial')
        personaesclavizada_initial = self.request.GET.get('personaesclavizada_initial')
        if documento_initial:
            initial['documento'] = documento_initial
        if personaesclavizada_initial:
            initial['persona'] = personaesclavizada_initial
        return initial

# Create views for  Vocabs
class CalidadesCreateView(CreateView):
    model = Calidades
    form_class = CalidadesForm
    template_name = 'esclavizados/Vocab/calidad.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_calidad'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/calidad.html']
        return ['esclavizados/Vocab/calidad.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'calidad_id': self.object.calidad_id,
                'calidad_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)

class HispanizacionesCreateView(CreateView):
    model = Hispanizaciones
    form_class = HispanizacionesForm
    template_name = 'esclavizados/Vocab/hispanizacion.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_hispanizacion'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/hispanizacion.html']
        return ['esclavizados/Vocab/hispanizacion.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'hispanizacion_id': self.object.hispanizacion_id,
                'hispanizacion_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)

class EtnonimosCreateView(CreateView):
    model = Etonimos
    form_class = EtnonimosForm
    template_name = 'esclavizados/Vocab/etnonimo.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_etnonimo'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/etnonimo.html']
        return ['esclavizados/Vocab/etnonimo.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'etnonimo_id': self.object.etonimo_id,
                'etnonimo_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)

class OcupacionesCreateView(CreateView):
    model = Actividades
    form_class = OcupacionesForm
    template_name = 'esclavizados/Vocab/ocupacion.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_ocupacion'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/ocupacion.html']
        return ['esclavizados/Vocab/ocupacion.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'ocupacion_id': self.object.actividad_id,
                'ocupacion_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)

# Browse Views

class ArchivoBrowse(ListView):
    model = Archivo
    template_name = 'esclavizados/Browse/archivos.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'updated_at')
        if sort not in ['archivo', 'created_at', 'titulo', 'tipo_documento', 'tipo_udc']:
            sort = '-updated_at'
        
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) | 
                Q(fondo__icontains=search_query)
            )
        
        return queryset.order_by(sort)

class DocumentoBrowse(ListView):
    model = Documento
    template_name = 'esclavizados/Browse/documentos.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'updated_at')
        if sort not in ['archivo', 'created_at', 'titulo', 'tipo_documento', 'tipo_udc']:
            sort = '-updated_at'
        
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) | 
                Q(fondo__icontains=search_query)
            )
        
        return queryset.order_by(sort)

class PersonaEsclavizadaBrowse(ListView):
    model = PersonaEsclavizada
    template_name = 'esclavizados/Browse/personasesclavizadas.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'updated_at')
        if sort not in ['nombres', 'created_at', 'apellidos', 'nombre_normalizado']:
            sort = '-updated_at'
        
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(nombres__icontains=search_query) | 
                Q(apellidos__icontains=search_query) |
                Q(nombre_normalizado__icontains=search_query)
            )
        
        return queryset.order_by(sort)

# Detail views

class ArchivoDetailView(DetailView):
    model = Archivo
    template_name = 'esclavizados/Detail/archivo.html'
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        archivo = self.get_object()
        
        documentos = Documento.objects.filter(
            models.Q(
                archivo = archivo
            )
        )
        
        context['documentos'] = documentos
        
        return context
    

class DocumentoDetailView(DetailView):
    model = Documento
    template_name = 'esclavizados/Detail/documento.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_history = self.object.history.first()
        history_records = self.object.history.all()
        context['history_records'] = history_records
        
        documento = self.get_object()
        
        peresclavizadas = PersonaEsclavizada.objects.filter(
            models.Q(
                documentos=documento
            )
        )
        
        personaesclavizadalugarrel = PersonaLugarRel.objects.filter(
            models.Q(
                documento=documento
            )
        )
        
        pernoesclavizadas = PersonaNoEsclavizada.objects.filter(
            models.Q(
                documentos=documento
            )
        )
        
        personapersonarel = PersonaRelaciones.objects.filter(
            models.Q(
                documento=documento
            )
        )
        
        context['peresclavizadas'] = peresclavizadas
        context['personaesclavizadalugarrel'] = personaesclavizadalugarrel
        context['pernoesclavizadas'] = pernoesclavizadas
        context['personapersonarel'] = personapersonarel
        
        last_updated_user = None
        if last_history:
            last_updated_user = last_history.history_user
        
        context['last_updated_user'] = last_updated_user
        
        return context

class PersonaEsclavizadaDetailView(DetailView):
    model = PersonaEsclavizada
    template_name = 'esclavizados/Detail/personaesclavizada.html'

# Update views

class ArchivoUpdateView(UpdateView):
    model = Archivo
    form_class = ArchivoForm
    template_name = 'esclavizados/Add/archivo.html'
    success_url = reverse_lazy('archivo-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(ArchivoUpdateView, self).get_form_kwargs()
        
        return kwargs
    
class DocumentoUpdateView(UpdateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'esclavizados/Add/documento.html' 
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(DocumentoUpdateView, self).get_form_kwargs()
        
        return kwargs


class PersonaEsclavizadaUpdateView(UpdateView):
    model = PersonaEsclavizada
    form_class = PersonaEsclavizadaForm
    template_name = 'esclavizados/Add/personaesclavizada.html' 
    success_url = reverse_lazy('personasesclavizadas-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PersonaEsclavizadaUpdateView, self).get_form_kwargs()
        
        return kwargs

# Delete views    

class ArchivoDeleteView(DeleteView):
    model = Archivo
    template_name = 'esclavizados/Base/archivo_confirm_delete.html'
    success_url = reverse_lazy('archivo-browse')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context
    
class DocumentoDeleteView(DeleteView):
    model = Documento
    template_name = 'esclavizados/Base/documento_confirm_delete.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context
    

class PersonaEsclavizadaDeleteView(DeleteView):
    model = Documento
    template_name = 'esclavizados/Base/personaesclavizada_confirm_delete.html'
    success_url = reverse_lazy('personasesclavizadas-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context