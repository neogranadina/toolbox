from django.db import transaction, models
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views import generic, View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from dal import autocomplete
from .models import Documento, Lugar, Persona, Matrimonio, Bautismo, Entierro, Relationship
from .forms import PersonaForm, DocumentoForm, LugarForm, RelationshipForm
from .forms import BautismoForm, MatrimonioForm, EntierroForm

import logging

logger = logging.getLogger("prosopographic")


def home(request):
    return render(request, 'prosopographic/home.html')

# Autocompletion views

class DocumentoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Documento.objects.all()
        if self.q:
            qs = qs.filter(titulo_documento__icontains=self.q)
            
        return qs

class LugarAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Lugar.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
            
        return qs

class PersonaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Persona.objects.all()
        if self.q:
            qs = qs.filter(nombre_completo__icontains=self.q)
            
        return qs

# general views
class DocumentoCreateView(CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'prosopographic/Form/documento.html'
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
            return ['prosopographic/Modals/documento_form_only.html']
        return ['prosopographic/Form/documento.html']
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.object = form.save()

        # Check if the request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return a JsonResponse with Documento data
            data = {
                'documento_id': self.object.id,
                'documento_name': str(self.object)  # Adjust the name as per your model's __str__ method
            }
            return JsonResponse(data)

        # For non-AJAX requests, redirect as usual
        return super().form_valid(form)
    
    def get_success_url(self):
        #return reverse_lazy('documento_detail', kwargs={'pk': self.object.pk})
        return reverse_lazy('home')


class LugarCreateView(CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'prosopographic/Form/lugar.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_lugar'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['prosopographic/Modals/lugar_form_only.html']
        return ['prosopographic/Form/lugar.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'lugar_id': self.object.id,
                'lugar_name': str(self.object)  
            }
            return JsonResponse(data)

        return super().form_valid(form)
    
    def get_success_url(self):
        #return reverse_lazy('lugar-detail', kwargs={'pk': self.object.pk})
        return reverse_lazy('home')


class PersonaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'prosopographic/Form/persona.html'
    success_url = reverse_lazy('persona-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_persona'] = context['form']
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['prosopographic/Modals/persona_form_only.html']
        return ['prosopographic/Form/persona.html']
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'persona_id': self.object.id,
                'persona_name': str(self.object)
            }
            return JsonResponse(data)

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('persona-detail', kwargs={'pk': self.object.pk})


class RelationshipCreateView(CreateView):
    model = Relationship
    form_class = RelationshipForm
    template_name = 'prosopographic/Form/relationship.html'
    success_url = reverse_lazy('persona-list')
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['prosopographic/Modals/relationship_form_only.html']
        return ['prosopographic/Form/relationship.html']
    
    def get_success_url(self):
        left_person_pk = self.object.left_person.pk
        return reverse_lazy('persona-detail', kwargs={'pk': left_person_pk})

# views for application
class BautismoCreateView(CreateView):
    model = Bautismo
    form_class = BautismoForm
    template_name = 'prosopographic/Form/bautismo.html'
    success_url = reverse_lazy('bautismo-browse') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context

    def get_success_url(self):
        return reverse_lazy('bautismo-detail', kwargs={'pk': self.object.pk})

class MatrimonioCreateView(CreateView):
    model = Matrimonio
    form_class = MatrimonioForm
    template_name = 'prosopographic/Form/matrimonio.html'
    success_url = reverse_lazy('matrimonio-browse')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('matrimonio-detail', kwargs={'pk': self.object.pk})
    
    
class EntierroCreateView(CreateView):
    model = Entierro
    form_class = EntierroForm
    template_name = 'prosopographic/Form/entierro.html'
    success_url = reverse_lazy('entierro-browse') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'añadir'
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('entierro-detail', kwargs={'pk': self.object.pk})

## Browse views

class DocumentoBrowse(ListView):
    paginate_by = 12
    model = Documento
    template_name = 'prosopographic/Browse/documentos.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'documento_idno')
        if sort not in ['documento_idno', 'titulo_documento']:
            sort = 'documento_idno'
        
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(titulo_documento__icontains=search_query) | 
                Q(documento_idno__icontains=search_query)
            )
        
        return queryset.order_by(sort)

class PersonaBrowse(ListView):
    paginate_by = 12
    model = Persona
    template_name = 'prosopographic/Browse/personas.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'apellidos')
        if sort not in ['nombre_completo', 'apellidos']:
            sort = 'nombre_completo'
        
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(nombre_completo__icontains=search_query)
            )
        
        return queryset.order_by(sort)

class LugarBrowse(ListView):
    paginate_by = 12
    model = Lugar
    template_name = 'prosopographic/Browse/lugares.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'nombre_lugar')
        if sort not in ['nombre_lugar', 'tipo']:
            sort = 'nombre_lugar'
        
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(nombre_lugar__icontains=search_query) | 
                Q(tipo__icontains=search_query)
            )
        
        return queryset.order_by(sort)

class BautismoBrowse(ListView):
    paginate_by = 12
    model = Bautismo
    template_name = 'prosopographic/Browse/bautismos.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'bautismo_idno')
        if sort not in ['bautismo_idno', 'acta_bautismo']:
            sort = 'bautismo_idno'
        
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(acta_bautismo__titulo_documento__icontains=search_query) | 
                Q(bautismo_idno__icontains=search_query) | 
                Q(bautizado__nombre_completo__icontains=search_query)
            )
        
        return queryset.order_by(sort)


class MatrimonioBrowse(ListView):
    paginate_by = 12
    model = Matrimonio
    template_name = 'prosopographic/Browse/matrimonios.html'

class EntierroBrowse(ListView):
    paginate_by = 12
    model = Entierro
    template_name = 'prosopographic/Browse/entierros.html'

## DEtail views

class DocumentoDetailView(DetailView):
    model = Documento
    template_name = 'prosopographic/Detail/documento.html'

class PersonaDetailView(DetailView):
    model = Persona
    template_name = 'prosopographic/Detail/persona.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        persona = self.get_object()

        bautizos = Bautismo.objects.filter(
            models.Q(bautizado=persona) | models.Q(padre=persona) | models.Q(madre=persona) |
            models.Q(padrino=persona) | models.Q(madrina=persona)
        )

        # Fetch relationships where the current persona is either left_person or right_person
        relationships = Relationship.objects.filter(
            models.Q(left_person=persona) | models.Q(right_person=persona)
        )

        # Adding relationships to context
        context['relationships'] = relationships
        context['bautismos'] = bautizos
        return context

class LugarDetailView(DetailView):
    model = Lugar
    template_name = 'prosopographic/Detail/lugar.html'

class BautismoDetailView(DetailView):
    model = Bautismo
    template_name = 'prosopographic/Detail/bautismo.html'

class MatrimonioDetailView(DetailView):
    model = Matrimonio
    template_name = 'prosopographic/Detail/matrimonio.html'
    
class EntierroDetailView(DetailView):
    model = Entierro
    template_name = 'prosopographic/Detail/entierro.html'
    
## Update views

class PersonaUpdateView(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'prosopographic/Form/persona.html' 
    success_url = reverse_lazy('persona-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PersonaUpdateView, self).get_form_kwargs()
        
        return kwargs

class BautismoUpdateView(UpdateView):
    model = Bautismo
    form_class = BautismoForm
    template_name = 'prosopographic/Form/bautismo.html' 
    success_url = reverse_lazy('bautismo-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(BautismoUpdateView, self).get_form_kwargs()
        
        return kwargs
    
class MatrimonioUpdateView(UpdateView):
    model = Matrimonio
    form_class = MatrimonioForm
    template_name = 'prosopographic/Form/matrimonio.html'
    success_url = reverse_lazy('matrimonio-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(MatrimonioUpdateView, self).get_form_kwargs()
        
        return kwargs
    
    
class EntierroUpdateView(UpdateView):
    model = Entierro
    form_class = EntierroForm
    template_name = 'prosopographic/Form/entierro.html'  # Use the same form template
    success_url = reverse_lazy('entierro-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'editar'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(EntierroUpdateView, self).get_form_kwargs()
        
        return kwargs
    
## Delete views

class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = 'prosopographic/Base/persona_confirm_delete.html'
    success_url = reverse_lazy('persona-browse')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context

class BautismoDeleteView(DeleteView):
    model = Bautismo
    template_name = 'prosopographic/Base/bautismo_confirm_delete.html'
    success_url = reverse_lazy('bautismo-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context

class MatrimonioDeleteView(DeleteView):
    model = Matrimonio
    template_name = 'prosopographic/Base/matrimonio_confirm_delete.html'
    success_url = reverse_lazy('matrimonio-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context

class EntierroDeleteView(DeleteView):
    model = Entierro
    template_name = 'prosopographic/Base/entierro_confirm_delete.html'
    success_url = reverse_lazy('entierro-browse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        context['action'] = 'borrar'
        return context