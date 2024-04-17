from django import forms
from .models import Bautismo, Matrimonio, Entierro, Documento, Persona, Lugar, Relationship
from datetime import datetime
from dal import autocomplete
import re

import logging

logger = logging.getLogger("prosopographic")

RELATIONSHIP_TYPES = (
        ('padre', 'es padre de'),
        ('madre', 'es madre de'),
        ('hijo', 'es hijo de'),
        ('legitimo', 'es hijo legítimo de'),
        ('natural', 'es hijo natural de'),
        ('hija', 'es hija de'),
        ('padrino', 'es padrino de'),
        ('madrina', 'es madrina de'),
        ('esposo', 'es esposo de'),
        ('esposa', 'es esposa de'),
        ('casado', 'está casado con'),
        ('hermano', 'es hermano de'),
        ('hermana', 'es hermana de'),
        ('ahijado', 'es ahijado de')
    )

ESTADO_DOCUMENTO = (
    ('bueno', 'Bueno'),
    ('regular', 'Regular'),
    ('malo', 'Malo')
)

ESTADOS_CONTRAYENTES = (
    ('solteria', 'Soltero/a'),
    ('viudez', 'Viudo/a'),
    ('casado', 'Casado'),
    ('desconocido', 'n/a')
)

LEGITIMIDAD_HIJO = (
    ('legitimo', 'Hijo legítimo'),
    ('natural', 'Hijo natural'),
    ('desconocida', 'n/a')
)

TIPOS_ENTERRAMIENTOS = (
    ('cruz_alta', 'Cruz Alta'),
    ('cruz_baja', 'Cruz Baja'),
    ('entierro_mayor', 'Entierro Mayor')
)

class CustomValidators:
    def validate_date(self, date_text):
        if not isinstance(date_text, str):
            return date_text
        date_text = date_text.strip()
        if len(date_text) > 10:
            raise forms.ValidationError(f"El formato de la fecha {date_text} es incorrecto. Use AAAA-MM-DD, AAAA-MM, o AAAA.")
        
        try:
            parsed_date = datetime.strptime(date_text, '%Y-%m-%d')
            return parsed_date.date()
        except ValueError:
            parts = date_text.split('-')
            if len(parts) == 1 and len(parts[0]) == 4:
                return datetime.strptime(date_text, '%Y').date()
            elif len(parts) == 2:
                return datetime.strptime(date_text, '%Y-%m').date()
            else:
                raise forms.ValidationError(f"El formato de la fecha {date_text} es incorrecto. Use AAAA-MM-DD, AAAA-MM, o AAAA.")

    def validate_folios(self, folio_inicial, folio_final):
        
        folio_inicial = str(folio_inicial)
        folio_final = str(folio_final) if folio_final else folio_inicial
        
        fininum = re.findall(r'^[1-9]\d*', folio_inicial)
        ffinnum = re.findall(r'^[1-9]\d*', folio_final)
        
        # Extract the first element from the list and convert to integer
        fininum = int(fininum[0])
        ffinnum = int(ffinnum[0])

        if ffinnum < fininum:
            raise forms.ValidationError(f"El valor de {folio_final} no puede ser menor que {folio_inicial}")
        elif fininum == ffinnum:
            folium_orientation_ini = re.findall(r"\w$", folio_inicial)
            folium_orientation_fin = re.findall(r"\w$", folio_final)
            if folium_orientation_ini != folium_orientation_fin:
                if folium_orientation_ini[0].lower() != 'r':
                    raise forms.ValidationError(f"La orientación de los folios ({folio_inicial} - {folio_final}) es incorrecta")


class CustomBuilders:
    def nacimiento_x_edad(self, edad, fecha_referencia):
        
        if edad and edad != "":
            anio = fecha_referencia.year
            fecha_nacimiento = anio - int(edad)
            return CustomValidators().validate_date(str(fecha_nacimiento))
        else:
            return None

    def edad_x_nacimiento(self, fecha_nacimiento, fecha_referencia):
        
        if fecha_nacimiento and fecha_nacimiento != "":
            anio_nac = fecha_nacimiento.year
            anio_ref = fecha_referencia.year
            
            edad = max(anio_ref, anio_nac) - min(anio_ref, anio_nac)
            return edad
        else:
            return None


class PersonaForm(forms.Form, forms.ModelForm):
    
    class Meta:
        model = Persona
        fields = '__all__'
        
    nombre = forms.CharField()
    apellidos = forms.CharField(required=False)
    nombre_completo = forms.CharField(required=False)
    condicion = forms.CharField(required=False)
    
    fecha_nacimiento = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )
    
    fecha_defuncion = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )
    
    lugar_nacimiento = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    
    vecindad = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    
    def save(self, *args, **kwargs):
        logger.debug("PersonaForm save method called.")
        
        persona = super().save(commit=False)
        
        persona.nombre = self.cleaned_data['nombre']
        persona.apellidos = self.cleaned_data['apellidos']
        persona.nombre_completo = self.cleaned_data['nombre_completo']
        persona.condicion = self.cleaned_data['condicion']
        persona.fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        persona.fecha_defuncion = self.cleaned_data['fecha_defuncion']
        persona.lugar_nacimiento = self.cleaned_data['lugar_nacimiento']
        persona.vecindad = self.cleaned_data['vecindad']
        
        persona.save()
        
        return persona


class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = '__all__'
        
    left_person = forms.ModelChoiceField(label="Persona 1",
        queryset=Persona.objects.all(), 
        required=True,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete')
    )
    
    relationship_type = forms.ChoiceField(required=True, label="Tipo de relación", choices=RELATIONSHIP_TYPES)
    
    right_person = forms.ModelChoiceField(label="Persona 2",
        queryset=Persona.objects.all(), 
        required=True,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete')
    )
    
    def save(self, commit=True):
        
        relation, create  = Relationship.objects.update_or_create(
            left_person = self.cleaned_data['left_person'],
            right_person = self.cleaned_data['right_person'],
            defaults={'relationship_type': self.cleaned_data['relationship_type']}
        )
        
        if commit:
            relation.save()
        
        return relation
    

class LugarForm(forms.Form, forms.ModelForm):
    class Meta:
        model = Lugar
        fields = '__all__'

class DocumentoForm(forms.Form, forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['unidad_documental', 'identificador', 'titulo_documento', 'notas']
    
    # Fields related to Documento
    folio_inicial = forms.CharField(max_length=50)
    folio_final = forms.CharField(max_length=50, required=False)
    imagen_inicial = forms.CharField(max_length=50)
    imagen_final = forms.CharField(max_length=50, required=False)
    estado_conservacion = forms.ChoiceField(choices=ESTADO_DOCUMENTO)
    
    def clean_folio_inicial(self):
        folio_inicial = self.cleaned_data.get('folio_inicial')
        if not folio_inicial or folio_inicial == "":
            raise forms.ValidationError(f"El valor del folio inicial no puede estar vacío.")
            
        pat = re.compile(r'^\d+[rv]$')
        
        if not re.fullmatch(pat, folio_inicial):
            raise forms.ValidationError(f"El formato de {folio_inicial} no es correcto.\nEj: 25r o 25v")
        
        return folio_inicial

    def clean_folio_final(self):
        folio_final = self.cleaned_data.get('folio_final')

        # If folio_final is empty, use folio_inicial as folio_final
        if not folio_final:
            folio_inicial = self.cleaned_data.get('folio_inicial', '')
            return folio_inicial

        # Validate the format of folio_final
        pat = re.compile(r'^\d+[rv]$')
        if not re.fullmatch(pat, folio_final):
            raise forms.ValidationError(f"El formato de {folio_final} no es correcto.\nEj: 25r o 25v")
        
        return folio_final
    
    def clean_imagen_final(self):
        imagen = self.cleaned_data.get('imagen_final')
        if imagen == "" or not imagen:
            return self.cleaned_data.get('imagen_inicial')
        
        return imagen
    
    def clean(self):
        cleaned_data = super().clean()
        folio_inicial = cleaned_data.get('folio_inicial')
        folio_final = cleaned_data.get('folio_final')
        try:
            CustomValidators().validate_folios(folio_inicial, folio_final)
        except forms.ValidationError as e:
            # Add the error to the form's error list
            self.add_error(None, e)
        
        return cleaned_data
    
    def save(self, commit=True):
        documento = super().save(commit=False)
        
        folio_inicial = self.cleaned_data['folio_inicial']
        folio_final = self.cleaned_data['folio_final']
        
        imagen_inicial = self.cleaned_data['imagen_inicial']
        imagen_final = self.cleaned_data['imagen_final']
        
        documento, created = Documento.objects.get_or_create(
        unidad_documental=self.cleaned_data['unidad_documental'],
        identificador=self.cleaned_data['identificador'],
        titulo_documento = self.cleaned_data['titulo_documento'],
        folios = f'{folio_inicial};{folio_final}',
        rango_imagenes = f'{imagen_inicial};{imagen_final}',
        notas = self.cleaned_data['notas'],
        condicion_documento = self.cleaned_data['estado_conservacion']
        )
        logger.debug(f"Documento created: {created}, Documento ID: {documento.id}")
        
        if commit:
            documento.save()
        return documento

class BautismoForm(forms.ModelForm):
    
    class Meta:
        model = Bautismo
        fields = '__all__'
    
    # Fields related to Bautismo
    acta_bautismo = forms.ModelChoiceField(queryset=Documento.objects.all(),
        widget=autocomplete.ModelSelect2(url='documento-autocomplete')
        )
    
    fecha_bautismo = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )
    lugar_bautismo = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    bautizado = forms.ModelChoiceField(
        queryset=Persona.objects.all(), 
        required=True,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete')
    )
    lugar_bautizado = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    fecha_nacimiento = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )
    condicion_bautizado = forms.ChoiceField(choices=LEGITIMIDAD_HIJO)

    # Fields to create related Persona instances
    padre = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Padre'
    )
    
    madre = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Madre'
    )
    
    padrino = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Padrino'
    )
    
    madrina = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Madrina'
    )
    
    bautizado_procedencia = forms.ModelChoiceField(
        queryset=Lugar.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete'),
        label='Procedencia del Bautizado'
    )

     
    def clean_lugar_bautismo(self):
        lugar_bautismo = self.cleaned_data.get('lugar_bautismo')
        if lugar_bautismo == "":
            return None
        
        return self.cleaned_data['lugar_bautismo']

    def clean(self):
        cleaned_data = super().clean()
        
        return cleaned_data

    def save(self, *args, **kwargs):
        logger.debug("BautismoForm save method called.")
        
        bautismo = super().save(commit=False)
        
        bautizado = self.cleaned_data['bautizado']
        if self.cleaned_data.get('fecha_nacimiento'):
            bautizado.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if self.cleaned_data.get('lugar_bautizado'):
            bautizado.lugar_nacimiento = self.cleaned_data.get('lugar_bautizado')
        bautizado.save()

        bautismo.bautizado=bautizado
        bautismo.lugar_bautismo= self.cleaned_data['lugar_bautismo']
        bautismo.fecha_bautismo=self.cleaned_data['fecha_bautismo']
        bautismo.padre = self.cleaned_data['padre']
        bautismo.madre = self.cleaned_data['madre']
        bautismo.padrino = self.cleaned_data['padrino']
        bautismo.madrina = self.cleaned_data['madrina']
        bautismo.lugar_bautismo = self.cleaned_data['lugar_bautismo']
        bautismo.bautizado_procedencia = self.cleaned_data['bautizado_procedencia']
        
        bautismo.save()
        
        return bautismo
    
    def __init__(self, *args, **kwargs):
        super(BautismoForm, self).__init__(*args, **kwargs)
        
        if 'instance' in kwargs and kwargs['instance'] is not None:
            instance = kwargs['instance']
            
            if instance.bautizado:
                bautizado = instance.bautizado
                self.fields['lugar_bautizado'].initial = bautizado.lugar_nacimiento
                self.fields['fecha_nacimiento'].initial = bautizado.fecha_nacimiento.strftime("%Y-%m-%d")
            
        for field_name, field in self.fields.items():
            initial_value = self.initial.get(field_name, 'Not set')
            logger.debug(f"Fiel: {field} Field name: {field_name}, Initial Value: {initial_value}")
        
    
class MatrimonioForm(forms.ModelForm):
    
    class Meta:
        model = Matrimonio
        fields = '__all__'
    
    acta_matrimonio = forms.ModelChoiceField(queryset=Documento.objects.all(),
        widget=autocomplete.ModelSelect2(url='documento-autocomplete')
        )
    
    fecha_matrimonio = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )
    
    lugar_matrimonio = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    
    # datos del contrayente
    esposo = forms.ModelChoiceField(
        queryset=Persona.objects.all(), 
        required=True,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete')
    )
    
    # additional fields to update esposo Persona
    
    estado_esposo = forms.ChoiceField(choices=ESTADOS_CONTRAYENTES)
    edad_esposo = forms.IntegerField(min_value=10, max_value=130, required=False, label="Edad del contrayente")
    natural_de_esposo = forms.ModelChoiceField(required=False,
        label="Procedencia (lugar de nacimiento) del contrayente",
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    residente_en_esposo = natural_de_esposo = forms.ModelChoiceField(required=False,
        label="Vecindad del contrayente",
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    legitimidad_esposo = forms.ChoiceField(choices=LEGITIMIDAD_HIJO, label="Condición de contrayente")
    
    # progenitores del contrayente
        
    padre_esposo = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Padre esposo'
    )
    
    madre_esposo = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Madre esposo'
    )
    
    # datos de la contrayente
    esposa = forms.ModelChoiceField(
        queryset=Persona.objects.all(), 
        required=True,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete')
    )
    
    # additional fields to update esposa Persona
    
    estado_esposa = forms.ChoiceField(choices=ESTADOS_CONTRAYENTES)
    edad_esposa = forms.IntegerField(min_value=10, max_value=130, required=False, label="Edad del contrayente")
    natural_de_esposa = forms.ModelChoiceField(required=False,
        label="Procedencia (lugar de nacimiento) del contrayente",
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    residente_en_esposa = natural_de_esposa = forms.ModelChoiceField(required=False,
        label="Vecindad del contrayente",
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    legitimidad_esposa = forms.ChoiceField(choices=LEGITIMIDAD_HIJO, label="Condición de contrayente")
    
    # progenitores del contrayente
        
    padre_esposa = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Padre esposa'
    )
    
    madre_esposa = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Madre esposa'
    )
    
    padrinos = forms.ModelMultipleChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='persona-autocomplete'),
        label='Padrinos'
    )

    testigos = forms.ModelMultipleChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='persona-autocomplete'),
        label='Testigos'
    )
        
    
    def clean_lugar_matrimonio(self):
        lugar_matrimonio = self.cleaned_data.get('lugar_matrimonio')
        if lugar_matrimonio == "":
            return None
        
        return self.cleaned_data['lugar_matrimonio']
    
    def clean_fecha_matrimonio(self):
        fecha_matrimonio = self.cleaned_data.get('fecha_matrimonio')
        
        if not fecha_matrimonio:
            logger.debug(f"Fecha de matrimonio not included: {fecha_matrimonio}")
            return None
        logger.debug(f"Cleaning fecha_matrimonio: {fecha_matrimonio}")
        fmclean = CustomValidators().validate_date(fecha_matrimonio)
        logger.debug(f"Fecha de matrimonio cleared: {fmclean}")
        return fmclean
    
    
    def clean(self):
        cleaned_data = super().clean()
        
        return cleaned_data
    
    def save(self, *args, **kwargs):
        logger.debug("MatrimonioForm save method called.")
        # Create Documento instance
        
        matrimonio = super().save(commit=False)
        
        esposo = self.cleaned_data['esposo']
        if self.cleaned_data.get('edad_esposo') and self.cleaned_data.get('fecha_matrimonio'):
            esposo.fecha_nacimiento = CustomBuilders().nacimiento_x_edad(self.cleaned_data.get('edad_esposo'), self.cleaned_data.get('fecha_matrimonio'))
        if self.cleaned_data.get('natural_de_esposo'):
            esposo.lugar_nacimiento = self.cleaned_data.get('natural_de_esposo')
        if self.cleaned_data.get('residente_en_esposo'):
            esposo.vecindad = self.cleaned_data.get('residente_en_esposo')
        esposo.save()


        esposa = self.cleaned_data['esposa']
        if self.cleaned_data.get('edad_esposa') and self.cleaned_data.get('fecha_matrimonio'):
            esposa.fecha_nacimiento = CustomBuilders().nacimiento_x_edad(self.cleaned_data.get('edad_esposa'), self.cleaned_data.get('fecha_matrimonio'))
        if self.cleaned_data.get('natural_de_esposa'):
            esposa.lugar_nacimiento = self.cleaned_data.get('natural_de_esposa')
        if self.cleaned_data.get('residente_en_esposa'):
            esposa.vecindad = self.cleaned_data.get('residente_en_esposa')
        esposa.save()
        
        
        matrimonio.acta_matrimonio = self.cleaned_data['acta_matrimonio']
        matrimonio.esposo = esposo
        matrimonio.esposa = esposa
        matrimonio.estado_esposo = self.cleaned_data['estado_esposo']
        matrimonio.estado_esposa = self.cleaned_data['estado_esposa']
        matrimonio.lugar = self.cleaned_data['lugar_matrimonio']
        matrimonio.fecha = self.cleaned_data['fecha_matrimonio']
        matrimonio.legitimidad_esposo = self.cleaned_data['legitimidad_esposo']
        matrimonio.legitimidad_esposa = self.cleaned_data['legitimidad_esposa']
        matrimonio.padre_esposo = self.cleaned_data['padre_esposo']
        matrimonio.madre_esposo = self.cleaned_data['madre_esposo']
        matrimonio.padre_esposa = self.cleaned_data['padre_esposa']
        matrimonio.madre_esposa = self.cleaned_data['madre_esposa']
        
        matrimonio.save()
        
        padrinos = self.cleaned_data.get('padrinos', [])
        if padrinos:
            matrimonio.padrinos.set(padrinos)

        testigos = self.cleaned_data.get('testigos', [])
        if testigos:
            matrimonio.testigos.set(testigos)
        logger.debug(f"Matrimonio instance saved: {matrimonio}")
        return matrimonio
    
    def __init__(self, *args, **kwargs):
        super(MatrimonioForm, self).__init__(*args, **kwargs)
        
        if 'instance' in kwargs and kwargs['instance'] is not None:
            instance = kwargs['instance']
            
            if instance.esposo:
                esposo = instance.esposo
                self.fields['edad_esposo'].initial = CustomBuilders().edad_x_nacimiento(esposo.fecha_nacimiento, instance.fecha_matrimonio)
                self.fields['natural_de_esposo'].initial = esposo.lugar_nacimiento
                self.fields['residente_en_esposo'].initial = esposo.vecindad
                            
            if instance.esposa:
                esposa = instance.esposa
                self.fields['edad_esposa'].initial = CustomBuilders().edad_x_nacimiento(esposa.fecha_nacimiento, instance.fecha_matrimonio)
                self.fields['natural_de_esposa'].initial = esposa.lugar_nacimiento
                self.fields['residente_en_esposa'].initial = esposa.vecindad

            
            for field_name, field in self.fields.items():
                initial_value = self.initial.get(field_name, 'Not set')
                logger.debug(f"Field: {field} Field name: {field_name}, Initial Value: {initial_value}")
    
class EntierroForm(forms.ModelForm):
    
    class Meta:
        model = Entierro
        fields = '__all__'
        
    acta_entierro = forms.ModelChoiceField(queryset=Documento.objects.all(),
        widget=autocomplete.ModelSelect2(url='documento-autocomplete')
        )
    
    fecha_entierro = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )
    lugar_declaracion = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    lugar_doctrina = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    tipo_entierro = forms.ChoiceField(choices=TIPOS_ENTERRAMIENTOS, label="Tipo de enterramiento")
    lugar_enterramiento = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    
    # Sobre el fallecimiento
    causa = forms.CharField(max_length=200, required=False)
    auxilio = forms.ChoiceField(choices=(('si', 'Si'),('no', 'No'),('desconocido', '---')), label="Recibió auxilio espiritual", required=False)
    
    # Datos del difunto
    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(), 
        required=True,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete')
    )
    procedencia_difunto = forms.ModelChoiceField(required=False,
        queryset=Lugar.objects.all(),
        widget=autocomplete.ModelSelect2(url='lugar-autocomplete')
    )
    edad_fallecimiento = forms.IntegerField(min_value=0, max_value=150, required=False)
    estado_difunto = forms.ChoiceField(choices=ESTADOS_CONTRAYENTES, label="Estado 'civil' del difunto")
    legitimidad_difunto = forms.ChoiceField(choices=LEGITIMIDAD_HIJO, label="Legitimidad")
    # Datos de los familiares
    padre = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Padre'
    )
    
    madre = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Madre'
    )
    
    # Datos cónyuge
    conyuge = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='persona-autocomplete'),
        label='Conyuge'
    )
    sobreviviente = forms.ChoiceField(choices=(('si', 'Si'),('no', 'No'),('desconocido', '---')), label="Sobrevive al fallecido", required=False)
    
    # denunciantes
    denunciantes = forms.ModelMultipleChoiceField(
        queryset=Persona.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='persona-autocomplete'),
        label='Denunciantes'
    )
    
    """ def clean_estado_difunto(self):
        estado_civil = self.cleaned_data.get('estado_difunto')
        conyuge = self.cleaned_data.get('conyuge')
        if conyuge and estado_civil == 'solteria':
            logger.warning(f"Error lógico en entierro de {self.cleaned_data.get('persona')}. Estado 'civil' no puede ser 'soltero' si hay un cónyuge [{conyuge}]. Modificado por 'casado'")
            return 'casado'
        
        return conyuge """
     
    
    def save(self, *args, **kwargs):
        logger.debug("EntierroForm save method called.")
        # Create Documento instance
        
        entierro = super().save(commit=False)
        
        fallecido = self.cleaned_data['persona']
        
        if self.cleaned_data.get('edad_fallecimiento') and self.cleaned_data.get('fecha_entierro'):
            fallecido.fecha_nacimiento = CustomBuilders().nacimiento_x_edad(self.cleaned_data.get('edad_fallecimiento'), self.cleaned_data.get('fecha_entierro'))
        if self.cleaned_data.get('fecha_entierro'):
            fallecido.fecha_defuncion = self.cleaned_data.get('fecha_entierro')
        if self.cleaned_data.get('procedencia_difunto'):
            fallecido.vecindad = self.cleaned_data.get('procedencia_difunto')
        fallecido.save()
        
        entierro.acta_entierro = self.cleaned_data['acta_entierro']
        entierro.persona = fallecido
        entierro.lugar = self.cleaned_data['lugar_enterramiento']
        entierro.lugar_declaracion = self.cleaned_data['lugar_declaracion']
        entierro.doctrina = self.cleaned_data['lugar_doctrina']
        entierro.fecha = self.cleaned_data['fecha_entierro']
        entierro.tipo_de_entierro = self.cleaned_data['tipo_entierro']
        entierro.legitimidad_difunto = self.cleaned_data['legitimidad_difunto']
        entierro.estado_difunto = self.cleaned_data['estado_difunto']
        
        entierro.padre = self.cleaned_data['padre']
        entierro.madre = self.cleaned_data['madre']
        entierro.conyuge = self.cleaned_data['conyuge']
        entierro.conyuge_sobrevive = self.cleaned_data['sobreviviente']
        entierro.causa_fallecimiento = self.cleaned_data['causa']
        entierro.auxilio_espiritual = self.cleaned_data['auxilio']
        
        entierro.save()
        
        denunciantes = self.cleaned_data.get('denunciantes', [])
        if denunciantes:
            entierro.denunciantes.set(denunciantes)
        
        logger.debug(f"Instance of entierro saved: {entierro}")
        return entierro
    
    def __init__(self, *args, **kwargs):
        super(EntierroForm, self).__init__(*args, **kwargs)
        
        if 'instance' in kwargs and kwargs['instance'] is not None:
            instance = kwargs['instance']

            # Sobre el fallecido

            if instance.persona:
                persona = instance.persona
                self.fields['edad_fallecimiento'].initial = CustomBuilders().edad_x_nacimiento(persona.fecha_nacimiento, instance.fecha)
        
        for field_name, field in self.fields.items():
                initial_value = self.initial.get(field_name, 'Not set')
                logger.debug(f"Field: {field} Field name: {field_name}, Initial Value: {initial_value}")
        