from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)

from collections import defaultdict

from dal import autocomplete

from .models import (Corporacion, Lugar, PersonaEsclavizada, PersonaNoEsclavizada, Documento, 
                     Archivo, Calidades, Hispanizaciones, Etonimos, Actividades,
                     PersonaLugarRel, Persona, PersonaRelaciones, PersonaRolEvento, Relationship, SituacionLugar,
                     TipoDocumental, RolEvento, TipoLugar, TiposInstitucion)

from .forms import (CorporacionForm, LugarForm, DocumentoForm, ArchivoForm, PersonaEsclavizadaForm,
                    PersonaNoEsclavizadaForm,
                    CalidadesForm, HispanizacionesForm, EtnonimosForm, OcupacionesForm,
                    PersonaLugarRelForm, PersonaRelacionesForm, PersonaRolEventoForm, RelationshipForm, RolesForm, SituacionLugarForm,
                    PersonaDocumentoForm, CorporacionDocumentoForm)

# Custom views

def home(request):
    return render(request, 'esclavizados/home.html')

def associate_persona_documento(request):
    if request.method == 'POST':
        form = PersonaDocumentoForm(request.POST)
        if form.is_valid():
            persona = form.cleaned_data['persona']
            documento = form.cleaned_data['documento']
            documento_id = documento.documento_id
            persona.documentos.add(documento)
            return redirect('documento-detail', pk=documento_id)
    else:
        documento_initial = request.GET.get('documento_initial')
        form = PersonaDocumentoForm(initial={'documento': documento_initial})
    return render(request, 'esclavizados/Relaciones/persona_x_documentos.html', {'form': form})

def associate_institucion_documento(request):
    if request.method == 'POST':
        form = CorporacionDocumentoForm(request.POST)
        if form.is_valid():
            institucion = form.cleaned_data['institucion']
            documento = form.cleaned_data['documento']
            documento_id = documento.documento_id
            institucion.documentos.add(documento)
            return redirect('documento-detail', pk=documento_id)
    else:
        documento_initial = request.GET.get('documento_initial')
        form = CorporacionDocumentoForm(initial={'documento': documento_initial})
    return render(request, 'esclavizados/Relaciones/institucion_x_documentos.html', {'form': form})

## Template views

class TotalBrowseView(TemplateView):
    """
    Mostrar todo a modo de Excel :p
    """
    template_name = 'esclavizados/Browse/todo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Documentos'] = Documento.objects.all()
        context['PersonasEsclavizadas'] = PersonaEsclavizada.objects.all()
        context['PersonasNoEsclavizadas'] = PersonaNoEsclavizada.objects.all()
        
        return context

class ConfirmRemovePersonaDocumento(TemplateView):
    template_name = 'esclavizados/Base/confirm_remove_persona_documento.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        persona = get_object_or_404(Persona, pk=kwargs['persona_id'])
        documento = get_object_or_404(Documento, pk=kwargs['documento_id'])
        persona.documentos.remove(documento)
        return redirect('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persona'] = get_object_or_404(Persona, pk=self.kwargs['persona_id'])
        context['documento'] = get_object_or_404(Documento, pk=self.kwargs['documento_id'])
        return context


## Generic Views

class LugarAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Lugar.objects.all().order_by('nombre_lugar')
        if self.q:
            qs = qs.filter(nombre_lugar__icontains=self.q)
            
        return qs

class PersonaEsclavizadaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        """ Search both in nombre_normalizado and in persona_idno
        """
        if not (self.request.user.is_authenticated and self.request.user.has_perm('dbgestor.view_personaesclavizada')):
            return PersonaEsclavizada.objects.none()
        qs = PersonaEsclavizada.objects.all().order_by('nombre_normalizado')
        if self.q:
            qs = qs.filter(
                Q(nombre_normalizado__icontains=self.q) |
                Q(persona_idno__icontains=self.q)
                )
            
        return qs

class PersonaNoEsclavizadaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        if not (self.request.user.is_authenticated and self.request.user.has_perm('dbgestor.view_personanoesclavizada')):
            return PersonaNoEsclavizada.objects.none()
        
        qs = PersonaNoEsclavizada.objects.all().order_by('nombre_normalizado')
        if self.q:
            qs = qs.filter(
                Q(nombre_normalizado__icontains=self.q) |
                Q(persona_idno__icontains=self.q)
                )
        return qs
    
class PersonaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        if not (self.request.user.is_authenticated and self.request.user.has_perm('dbgestor.view_persona')):
            return Persona.objects.none()
        
        qs = Persona.objects.all().order_by('nombre_normalizado')
        if self.q:
            qs = qs.filter(
                Q(nombre_normalizado__icontains=self.q) |
                Q(persona_idno__icontains=self.q)
                )
        return qs

class InstitucionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not (self.request.user.is_authenticated and self.request.user.has_perm('dbgestor.view_corporacion')):
            return Corporacion.objects.none()
        
        qs = Corporacion.objects.all().order_by('nombre_institucion')
        if self.q:
            qs = qs.filter(
                Q(nombre_institucion__icontains=self.q) |
                Q(corporacion_idno__icontains=self.q)
            )
        return qs

class DocumentoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Documento.objects.all().order_by('titulo')
        if self.q:
            qs = qs.filter(titulo__icontains=self.q)
        return qs


class ArchivoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Archivo.objects.all().order_by('nombre')
        if self.q:
            qs = qs.filter(
                Q(nombre__icontains=self.q) |
                Q(nombre_abreviado__icontains=self.q)
            )
        return qs
    

class FondoAutocomplete(autocomplete.Select2QuerySetView):
    def get_context_data(self, **kwargs):
        pass
    
class CalidadesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Calidades.objects.all().order_by('calidad')

        if self.q:
            qs = qs.filter(calidad__icontains=self.q)
            
        return qs
    
class CalidadesPersonaEsclavizadaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        calidades_ids = Calidades.objects.filter(
            persona__personaesclavizada__isnull=False
        ).values_list('calidad_id', flat=True).distinct()

        qs = Calidades.objects.filter(calidad_id__in=calidades_ids).order_by('calidad')

        if self.q:
            qs = qs.filter(calidad__icontains=self.q)

        return qs

class CalidadesPersonasNoEsclavizadasAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        calidades_ids = Calidades.objects.filter(
            persona__personanoesclavizada__isnull=False
            ).values_list('calidad_id', flat=True).distinct()
        
        qs = Calidades.objects.filter(calidad_id__in=calidades_ids).order_by('calidad')
        
        if self.q:
            qs = qs.filter(calidad__icontains=self.q)

        return qs

class HispanizacionesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Hispanizaciones.objects.all().order_by('hispanizacion')
        if self.q:
            qs = qs.filter(hispanizacion__icontains=self.q)
        return qs

class EtnonimosAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Etonimos.objects.all().order_by('etonimo')
        if self.q:
            qs = qs.filter(etonimo__icontains=self.q)
        return qs

class OcupacionesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Actividades.objects.all().order_by('actividad')

        if self.q:
            qs = qs.filter(actividad__icontains=self.q)
        return qs


class SituacionLugarAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SituacionLugar.objects.all().order_by('situacion')
        if self.q:
            qs = qs.filter(situacion__icontains=self.q)
        return qs

class TipoDocumentalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = TipoDocumental.objects.all().order_by('tipo_documental')
        if self.q:
            qs = qs.filter(tipo_documental__icontains=self.q)
        return qs

class RolEventoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RolEvento.objects.all().order_by('rol_evento')
        if self.q:
            qs = qs.filter(rol_evento__icontains=self.q)
        return qs

class TipoLugarAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = TipoLugar.objects.all().order_by('tipo_lugar')
        if self.q:
            qs = qs.filter(tipo_lugar__icontains=self.q)
        return qs

class TiposInstitucionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = TiposInstitucion.objects.all().order_by('tipo')
        if self.q:
            qs = qs.filter(tipo__icontains=self.q)
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
    success_url = reverse_lazy('home_esc')

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
        self.object = form.save(commit=False)
        
        self.object.fecha_inicial_aproximada = self.request.POST.get('fecha_inicial_aproximada', '') == 'on'
        self.object.fecha_final_aproximada = self.request.POST.get('fecha_final_aproximada', '') == 'on'
        
        self.object.save()

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

    def get_initial(self):
        initial = super().get_initial()
        
        archivo_initial = self.request.GET.get('archivo_initial')
        if archivo_initial:
            initial['archivo'] = archivo_initial
            
        return initial


class LugarCreateView(CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'esclavizados/Add/lugar.html'
    success_url = reverse_lazy('home_esc')

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
        return reverse_lazy('home_esc')
    

class PersonaEsclavizadaCreateView(CreateView):
    model = PersonaEsclavizada
    form_class = PersonaEsclavizadaForm
    template_name = 'esclavizados/Add/personaesclavizada.html'
    success_url = reverse_lazy('personasesclavizadas-browse')
    
    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        next_url = self.request.POST.get('next')
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        elif next_url:
            return reverse(next_url)
        else:
            return reverse('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next')
        if next_url:
            context['next'] = next_url
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            initial['documentos'] = documento_initial
        
        return initial

class PersonaNoEsclavizadaCreateView(CreateView):
    model = PersonaNoEsclavizada
    form_class = PersonaNoEsclavizadaForm
    template_name = 'esclavizados/Add/personanoesclavizada.html'
    success_url = reverse_lazy('personasnoesclavizadas-browse')
    
    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        else:
            return reverse('documento-browse')
    
    def get_initial(self):
        initial = super().get_initial()
        
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            initial['documentos'] = documento_initial
        
        return initial


class CoporacionCreateView(CreateView):
    model = Corporacion
    form_class = CorporacionForm
    template_name = 'esclavizados/Add/institucion.html'
    success_url = reverse_lazy('corporaciones-browse')
    
    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        else:
            return reverse('documento-browse')
    
    def get_initial(self):
        initial = super().get_initial()
        
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            initial['documentos'] = documento_initial
        
        return initial

# create views for RElations

class PersonaLugarRelCreateView(CreateView):
    model = PersonaLugarRel
    form_class = PersonaLugarRelForm
    template_name = 'esclavizados/Relaciones/persona_x_lugar.html'
    success_url = reverse_lazy('documento-browse')

    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        else:
            return reverse('documento-browse')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        personas_initial = self.request.GET.get('ids')
        if personas_initial:
            personas_ids = personas_initial.split(',')
            selected_personas = Persona.objects.filter(persona_id__in=personas_ids)
            form.fields['personas'].initial = selected_personas
        return form
    
    def get_initial(self):
        initial = super().get_initial()
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            initial['documento'] = documento_initial
        return initial

    def form_valid(self, form):
        response = super().form_valid(form) 
        return response

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
        
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        personas_initial = self.request.GET.get('ids')
        if personas_initial:
            personas_ids = personas_initial.split(',')
            selected_personas = Persona.objects.filter(persona_id__in=personas_ids)
            form.fields['personas'].initial = selected_personas
        return form
        
    def get_initial(self):
        initial = super().get_initial()
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            initial['documento'] = documento_initial
        return initial

    def form_valid(self, form):
        response = super().form_valid(form) 
        return response

class RelationshipCreateView(CreateView):
    model = Relationship
    form_class = RelationshipForm
    template_name = 'esclavizados/Add/relacion.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Add/relacion.html']
        return ['esclavizados/Add/relacion.html']
    
    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        else:
            return reverse('documento-browse')

class PersonaRolEventoCreateView(CreateView):
    model = PersonaRolEvento
    form_class = PersonaRolEventoForm
    template_name = 'esclavizados/Relaciones/rol_evento.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_success_url(self):
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            return reverse('documento-detail', kwargs={'pk': documento_initial})
        else:
            return reverse('documento-browse')
        
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        personas_initial = self.request.GET.get('ids')
        if personas_initial:
            personas_ids = personas_initial.split(',')
            selected_personas = Persona.objects.filter(persona_id__in=personas_ids)
            form.fields['personas'].initial = selected_personas
        return form
        
    def get_initial(self):
        initial = super().get_initial()
        documento_initial = self.request.GET.get('documento_initial')
        if documento_initial:
            initial['documento'] = documento_initial
        return initial

    def form_valid(self, form):
        response = super().form_valid(form) 
        return response

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


class SituacionLugarCreateView(CreateView):
    model = SituacionLugar
    form_class = SituacionLugarForm
    template_name = 'esclavizados/Vocab/situacion_lugar.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_situacion'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/situacion_lugar.html']
        return ['esclavizados/Vocab/situacion_lugar.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'situacion_id': self.object.situacion_id,
                'situacion_lugar_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)

class RolesCreateView(CreateView):
    model = RolEvento
    form_class = RolesForm
    template_name = 'esclavizados/Vocab/rol.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_rol'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['esclavizados/Modals/rol.html']
        return ['esclavizados/Vocab/rol.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'id': self.object.id,
                'rol_evento_name': str(self.object) 
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)


# Browse Views

class ArchivoBrowse(ListView):
    paginate_by = 12
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
    paginate_by = 12
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
    paginate_by = 12
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


class PersonaNoEsclavizadaBrowse(ListView):
    paginate_by = 12
    model = PersonaNoEsclavizada
    template_name = 'esclavizados/Browse/personasnoesclavizadas.html'
    
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

class CorporacionBrowse(ListView):
    paginate_by = 12
    model = Corporacion
    template_name = 'esclavizados/Browse/corporaciones.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'updated_at')
        if sort not in ['tipo_institucion', 'created_at', 'nombre_institucion']:
            sort = '-updated_at'
        
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(tipo_institucion__icontains=search_query) |
                Q(nombre_institucion__icontains=search_query)
            )
        
        return queryset.order_by(sort)

# Detail views

class ArchivoDetailView(DetailView):
    model = Archivo
    template_name = 'esclavizados/Detail/archivo.html'
    
    def get_context_data(self, **kwargs):
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
        history_records = self.object.history.all()
        context['history_records'] = history_records
        
        documento = self.get_object()
        
        peresclavizadas = PersonaEsclavizada.objects.filter(
            models.Q(
                documentos=documento
            )
        )
        
        personalugarrel = PersonaLugarRel.objects.filter(
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
        
        corporacionrel = Corporacion.objects.filter(
            models.Q(
                documentos=documento
            )
        )
        
        personarolrel = PersonaRolEvento.objects.filter(
            models.Q(
                documento=documento
            )
        )
        
        relationship_data = defaultdict(list)
        
        for relacion in personapersonarel:
            naturaleza_rel = relacion.get_naturaleza_relacion_display()
            relacion_data = {
                'id_rel': relacion.persona_relacion_id,
                'personas': [],
            }
            for persona in relacion.personas.all():
                relacion_data['personas'].append({
                    'nombre': persona.nombre_normalizado,
                    'idno': persona.persona_idno,
                    'id': persona.persona_id,
                })
            relationship_data[naturaleza_rel].append(relacion_data)
        
        place_data = defaultdict(lambda: defaultdict(dict))

        for rel in personalugarrel:
            category = "Anteriores" if rel.ordinal < 1 else "Posteriores"
            place_name = rel.lugar.nombre_lugar
            place_id = rel.lugar.lugar_id
            id_relacion = rel.persona_x_lugares
            if place_name not in place_data[category]:
                place_data[category][place_name] = {'personas': [], 'ordinal': rel.ordinal, 'rel_id': id_relacion, 'place_id': place_id}
            for persona in rel.personas.all():
                place_data[category][place_name]['personas'].append(persona.persona_idno)
        
        for category in place_data:
            sorted_places = sorted(place_data[category].items(), key=lambda x: x[1]['ordinal'])
            place_data[category] = dict(sorted_places)
        
        place_data_standard = {category: dict(places) for category, places in place_data.items()}
        
        rol_data = defaultdict(list)
        
        for rol in personarolrel:
            rol_evento = rol.rol_evento
            id_rol = rol.id
            for persona in rol.personas.all():
                rol_data[persona.persona_id].append({
                    'nombre': persona.nombre_normalizado,
                    'idno': persona.persona_idno,
                    'rol_evento': str(rol_evento),
                    'id_relacion': id_rol
                })
                    
        
        context['peresclavizadas'] = peresclavizadas
        context['personalugarrel'] = personalugarrel
        context['pernoesclavizadas'] = pernoesclavizadas
        context['corporacionrel'] = corporacionrel
        context['personapersonarel'] = personapersonarel
        context['relationshipdata'] = dict(relationship_data)
        context['place_data'] = place_data_standard
        context['personarolrel'] = dict(rol_data)
        
        return context

class PersonaEsclavizadaDetailView(DetailView):
    model = PersonaEsclavizada
    template_name = 'esclavizados/Detail/personaesclavizada.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        history_records = self.object.history.all()
        context['history_records'] = history_records
        
        personaesclavizada = self.get_object()
        
        personalugarrel = PersonaLugarRel.objects.filter(
            models.Q(
                personas=personaesclavizada
            )
        ).order_by('documento__fecha_inicial')
        
        ordered_places = []
        for rel in personalugarrel:
            ordered_places.append((rel.documento.fecha_inicial, rel.ordinal, rel.lugar, rel.documento))
            
        ordered_places.sort(key=lambda x: (x[0], x[1]))
        ordered_places_list = [(place[2], place[3]) for place in ordered_places]
        
        personapersonarel = PersonaRelaciones.objects.filter(
            models.Q(
                personas=personaesclavizada
            )
        ).order_by('naturaleza_relacion')
        
        corporacionrel = Corporacion.objects.filter(
            models.Q(
                personas_asociadas=personaesclavizada
            )
        )
        
        context['personalugarrel'] = personalugarrel
        context['ordered_places'] = ordered_places_list
        context['personapersonarel'] = personapersonarel
        context['corporaciones'] = corporacionrel
        
        return context
        

class PersonaNoEsclavizadaDetailView(DetailView):
    model = PersonaNoEsclavizada
    template_name = 'esclavizados/Detail/personanoesclavizada.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_history = self.object.history.first()
        history_records = self.object.history.all()
        context['history_records'] = history_records
        
        personanoesclavizada = self.get_object()
        
        personalugarrel = PersonaLugarRel.objects.filter(
            models.Q(
                personas=personanoesclavizada
            )
        ).order_by('documento__fecha_inicial')
        
        ordered_places = []
        for rel in personalugarrel:
            ordered_places.append((rel.documento.fecha_inicial, rel.ordinal, rel.lugar, rel.documento))
            
        ordered_places.sort(key=lambda x: (x[0], x[1]))
        ordered_places_list = [(place[2], place[3]) for place in ordered_places]
        
        personapersonarel = PersonaRelaciones.objects.filter(
            models.Q(
                personas=personanoesclavizada
            )
        )
        
        corporacionrel = Corporacion.objects.filter(
            models.Q(
                personas_asociadas=personanoesclavizada
            )
        )
        
        context['personalugarrel'] = personalugarrel
        context['personapersonarel'] = personapersonarel
        context['ordered_places'] = ordered_places_list
        context['corporaciones'] = corporacionrel
        
        return context

class CorporacionDetailView(DetailView):
    model = Corporacion
    template_name = "esclavizados/Detail/institucion.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_history = self.object.history.first()
        history_records = self.object.history.all()
        context['history_records'] = history_records
        
        corporacion = self.get_object()
    
        return context
    

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

class PersonaNoEsclavizadaUpdateView(UpdateView):
    model = PersonaNoEsclavizada
    form_class = PersonaNoEsclavizadaForm
    template_name = 'esclavizados/Add/personanoesclavizada.html' 
    success_url = reverse_lazy('personasnoesclavizadas-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PersonaNoEsclavizadaUpdateView, self).get_form_kwargs()
        
        return kwargs


class CorporacionUpdateView(UpdateView):
    model = Corporacion
    form_class = CorporacionForm
    template_name = 'esclavizados/Add/institucion.html'
    success_url = reverse_lazy('instituciones_browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(CorporacionUpdateView, self).get_form_kwargs()
        return kwargs

class PersonaLugarRelUpdateView(UpdateView):
    model = PersonaLugarRel
    form_class = PersonaLugarRelForm
    template_name = 'esclavizados/Relaciones/persona_x_lugar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PersonaLugarRelUpdateView, self).get_form_kwargs()
        return kwargs
    
    def form_valid(self, form):
        self.object = form.save()
        documento_id = self.request.POST.get('documento')
        return redirect('documento-detail', pk=documento_id)

class PersonaRelacionesUpdateView(UpdateView):
    model = PersonaRelaciones
    form_class = PersonaRelacionesForm
    template_name = 'esclavizados/Relaciones/persona_x_persona.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PersonaRelacionesUpdateView, self).get_form_kwargs()
        return kwargs
    
    def form_valid(self, form):
        self.object = form.save()
        documento_id = self.request.POST.get('documento')
        return redirect('documento-detail', pk=documento_id)




# Delete views  

class ArchivoDeleteView(DeleteView):
    model = Archivo
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('archivo-browse')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context
    
class DocumentoDeleteView(DeleteView):
    model = Documento
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context
    

class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('documento-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context

class PersonaEsclavizadaDeleteView(DeleteView):
    model = PersonaEsclavizada
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('personasesclavizadas-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context
    
class PersonaNoEsclavizadaDeleteView(DeleteView):
    model = PersonaNoEsclavizada
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('personasnoesclavizadas-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context  
    

class CorporacionDeleteView(DeleteView):
    model = Corporacion
    template_name = "esclavizados/Base/confirm_delete.html"
    success_url = reverse_lazy('instituciones_browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context

# Delete Vocabs
class PersonaLugarRelDeleteView(DeleteView):
    model = PersonaLugarRel
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('documentos-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context  
    

class DeletePersonaRelacionesView(DeleteView):
    model = PersonaRelaciones
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('documento-browse')
    
class DeletePersonaLugarRelView(DeleteView):
    model = PersonaLugarRel
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('documento-browse')
    
class DeleteRolEventoView(DeleteView):
    model = PersonaRolEvento
    template_name = 'esclavizados/Base/confirm_delete.html'
    success_url = reverse_lazy('documento-browse')