from django.db import models
from simple_history.models import HistoricalRecords
import json

import logging

logger = logging.getLogger("prosopographic")

class Archivo(models.Model):
    
    archivo_id = models.AutoField(primary_key=True)
    archivo_idno = models.CharField(max_length=50, null=True, blank=True)
    
    archivo_nombre = models.CharField(max_length=200)
    archivo_sigla = models.CharField(max_length=50, null=True, blank=True)
    
    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
        if self.archivo_id:
            self.archivo_idno = f"arc-{str(self.archivo_id).zfill(6)}"
        super(Archivo, self).save(*args, **kwargs)
        if not self.archivo_id: 
            self.archivo_idno = f"arc-{str(self.archivo_id).zfill(6)}"
            super(Archivo, self).save(*args, **kwargs)

    
    def __str__(self):
        return f"[{self.archivo_idno}.{self.archivo_nombre}] {self.archivo_sigla}"

class Documento(models.Model):
    
    documento_id = models.AutoField(primary_key=True)
    documento_idno = models.CharField(max_length=50, null=True, blank=True)
    
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE, related_name='archivado_en')
    
    unidad_documental = models.CharField(max_length=100)
    identificador = models.CharField(max_length=50)
    titulo_documento = models.CharField(max_length=100)
    folios = models.TextField() # this one will store an array of two elements of this shape [3r,4v]
    rango_imagenes = models.TextField() # this one will store an array of multiple images names or paths
    
    notas = models.TextField(null=True, blank=True)
    condicion_documento = models.CharField(max_length=200, null=True, blank=True)
    
    history = HistoricalRecords()
    
    def get_folios_json(self):
        return json.loads(self.folios)

    def set_folios_json(self, value):
        self.folios = json.dumps(value)

    def get_rango_imagenes_json(self):
        return json.loads(self.rango_imagenes)

    def set_rango_imagenes_json(self, value):
        self.rango_imagenes = json.dumps(value)
    
    def save(self, *args, **kwargs):
        
        if self.documento_id:
            self.documento_idno = f"doc-{str(self.documento_id).zfill(6)}"
        super(Documento, self).save(*args, **kwargs)
        if not self.documento_id: 
            self.documento_idno = f"doc-{str(self.documento_id).zfill(6)}"
            super(Documento, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"[{self.unidad_documental}.{self.identificador}] {self.titulo_documento}"
    
    
class Lugar(models.Model):
    
    lugar_id = models.AutoField(primary_key=True)
    lugar_idno = models.CharField(max_length=50, null=True, blank=True)
    
    nombre = models.CharField(max_length=100)
    otros_nombres = models.TextField(null=True, blank=True) # array with all place alternatives names.
    tipo = models.CharField(max_length=200, null=True, blank=True) # e.g., Country, State, City
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # ... other place details ...
    
    history = HistoricalRecords()
    
    def get_otros_nombres_json(self):
        return json.loads(self.other_names)

    def set_other_names_json(self, value):
        self.other_names = json.dumps(value)
    
    def save(self, *args, **kwargs):
        if self.lugar_id:
            self.lugar_idno = f"lug-{str(self.lugar_id).zfill(6)}"
        super(Lugar, self).save(*args, **kwargs)
        if not self.lugar_id: 
            self.lugar_idno = f"lug-{str(self.lugar_id).zfill(6)}"
            super(Lugar, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"{self.nombre}"

class Persona(models.Model):
    
    persona_id = models.AutoField(primary_key=True)
    persona_idno = models.CharField(max_length=50, null=True, blank=True)
    
    persona_import_identifier = models.CharField(max_length=100, null=True, blank=True)
    
    # Add basic person details (name, birthdate, etc.)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100, null=True)
    nombre_completo = models.CharField(max_length=200, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    notas_fecha_nacimiento = models.CharField(max_length=100, blank=True, null=True, help_text="Fechas incompletas, incorrectas o anotaciones.")
    fecha_defuncion = models.DateField(null=True, blank=True)
    notas_fecha_defuncion = models.CharField(max_length=100, blank=True, null=True, help_text="Fechas incompletas, incorrectas o anotaciones.")
    
    lugar_nacimiento = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='nacidos_en', null=True, blank=True)
    vecindad = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='residentes', null=True, blank=True)

    # person condition
    condicion = models.CharField(max_length=100, null=True, blank=True)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Update the full name whenever the instance is saved
        self.nombre_completo = f"{self.nombre} {self.apellidos}".strip()
        if self.persona_id:
            self.persona_idno = f"per-{str(self.persona_idno).zfill(6)}"
        super(Persona, self).save(*args, **kwargs)
        if not self.persona_id: 
            self.persona_idno = f"per-{str(self.persona_idno).zfill(6)}"
            super(Persona, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nombre_completo}"


class Relationship(models.Model):
    
    left_person = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='relacionado_con')
    relationship_type = models.CharField(max_length=50)
    right_person = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='con_relacionado')
    
    def __str__(self):
        return f"{self.left_person} {self.relationship_type} {self.right_person}"

class Bautismo(models.Model):
    
    bautismo_id = models.AutoField(primary_key=True)
    bautismo_idno = models.CharField(max_length=50, null=True, blank=True)
    acta_bautismo = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='acta_bautismo', null=True)
    
    bautizado = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='bautismos')
    lugar_bautismo = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='bautismos_como_lugar', null=True)
    fecha_bautismo = models.DateField(null=True, blank=True)
    notas_fecha_bautismo = models.CharField(max_length=100, blank=True, null=True, help_text="Fechas incompletas, incorrectas o anotaciones.")
    bautizado_procedencia = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='bautismos_como_procedencia', null=True)
    padre = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='hijos_bautizados', null=True, blank=True)
    madre = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='hijos_bautizados_madre', null=True, blank=True)
    padrino = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='ahijados_padrino', null=True, blank=True)
    madrina = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='ahijados_madrina', null=True, blank=True)
    
    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
        
        self.bautismo_idno = f"bau-{str(self.bautismo_idno).zfill(6)}"
        
        super(Bautismo, self).save(*args, **kwargs)
        if self.padre:
            Relationship.objects.update_or_create(left_person=self.padre, relationship_type='padre', right_person=self.bautizado)
            Relationship.objects.update_or_create(left_person=self.bautizado, relationship_type='hijo', right_person=self.padre)
        if self.madre:
            Relationship.objects.update_or_create(left_person=self.madre, relationship_type='madre', right_person=self.bautizado)
            Relationship.objects.update_or_create(left_person=self.bautizado, relationship_type='hijo', right_person=self.madre)
        if self.padre and self.madre:
            Relationship.objects.update_or_create(
                left_persona=self.padre, relationship_type='esposo', right_person=self.madre)
            Relationship.objects.update_or_create(
                left_persona=self.madre, relationship_type='esposa', right_person=self.padre)
            
        if self.padrino:
            Relationship.objects.update_or_create(left_person=self.padrino, relationship_type='padrino', right_person=self.bautizado)
            Relationship.objects.update_or_create(left_person=self.bautizado, relationship_type='ahijado', right_person=self.padrino)
        if self.madrina:
            Relationship.objects.update_or_create(left_person=self.madrina, relationship_type='madrina', right_person=self.bautizado)
            Relationship.objects.update_or_create(left_person=self.bautizado, relationship_type='ahijado', right_person=self.madrina)
    
    # ... other baptism details ...
    
    def __str__(self):
        return f"{self.bautizado}"

class Matrimonio(models.Model):
    
    matrimonio_id = models.AutoField(primary_key=True)
    matrimonio_idno = models.CharField(max_length=50, null=True, blank=True)
    
    acta_matrimonio = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='acta_matrimonio', null=True)

    fecha_matrimonio = models.DateField()
    notas_fecha_matrimonio = models.CharField(max_length=100, blank=True, null=True, help_text="Fechas incompletas, incorrectas o anotaciones.")
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, null=True, blank=True)
    
    esposo = models.ForeignKey(Persona, related_name='esposos', on_delete=models.CASCADE, null=True)
    estado_esposo = models.CharField(max_length=100) # f.i. soltero, viudo.
    legitimidad_esposo = models.CharField(max_length=50, null=True) # hijo legítimo, hijo natural
    
    padre_esposo = models.ForeignKey(Persona, related_name='padre_esposos', on_delete=models.CASCADE, null=True)
    madre_esposo = models.ForeignKey(Persona, related_name='madre_esposos', on_delete=models.CASCADE, null=True)
    
    esposa = models.ForeignKey(Persona, related_name='esposas', on_delete=models.CASCADE, null=True)
    estado_esposa = models.CharField(max_length=100) # f.i. soltero, viudo.
    legitimidad_esposa = models.CharField(max_length=50, null=True) # hijo legítimo, hijo natural
    
    padre_esposa = models.ForeignKey(Persona, related_name='padre_esposas', on_delete=models.CASCADE, null=True)
    madre_esposa = models.ForeignKey(Persona, related_name='madre_esposas', on_delete=models.CASCADE, null=True)
    
    padrinos = models.ManyToManyField(Persona, related_name='padrinos', blank=True)
    testigos = models.ManyToManyField(Persona, related_name='testigos', blank=True)
    
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.matrimonio_idno = f"mat-{str(self.matrimonio_idno).zfill(6)}"
        super(Matrimonio, self).save(*args, **kwargs)
        
        if self.legitimidad_esposo == 'desconocida':
            relationship_type_esposo = "hijo"
        else:
            logger.debug(f"Legitimidad of {self.esposo}: {self.legitimidad_esposo}")
            relationship_type_esposo = self.legitimidad_esposo
            
        if self.legitimidad_esposa == 'desconocida':
            relationship_type_esposa = "hija"
        else:
            logger.debug(f"Legitimidad of {self.esposa}: {self.legitimidad_esposa}")
            relationship_type_esposa = self.legitimidad_esposa
        
        if self.esposo and self.esposa:
            Relationship.objects.update_or_create(left_person=self.esposo, relationship_type='esposo', right_person=self.esposa)
            Relationship.objects.update_or_create(left_person=self.esposa, relationship_type='esposa', right_person=self.esposo)
        
        if self.esposo and self.padre_esposo:
            Relationship.objects.update_or_create(
                left_person=self.esposo,
                right_person=self.padre_esposo,
                defaults={'relationship_type': relationship_type_esposo}
            )
            Relationship.objects.update_or_create(
                left_person=self.padre_esposo,
                right_person=self.esposo,
                defaults={'relationship_type': 'padre'}
            )
        if self.esposo and self.madre_esposo:
            Relationship.objects.update_or_create(
                left_person=self.esposo, 
                right_person=self.madre_esposo,
                defaults={'relationship_type': relationship_type_esposo}
            )
            Relationship.objects.update_or_create(
                left_person=self.madre_esposo,  
                right_person=self.esposo,
                defaults={'relationship_type': 'madre'}
            )
        
        if self.esposa and self.padre_esposa:
            Relationship.objects.update_or_create(
                left_person=self.esposa,
                right_person=self.padre_esposa,
                defaults={'relationship_type': relationship_type_esposa}
            )
            Relationship.objects.update_or_create(
                left_person=self.padre_esposa, 
                right_person=self.esposa,
                defaults={'relationship_type': 'padre'}
            )
        if self.esposa and self.madre_esposa:
            Relationship.objects.update_or_create(
                left_person=self.esposa, 
                right_person=self.madre_esposa,
                defaults={'relationship_type': relationship_type_esposa}
            )
            Relationship.objects.update_or_create(
                left_person=self.madre_esposa,
                right_person=self.esposa,
                defaults={'relationship_type': 'madre'}
            )

    def __str__(self) -> str:
        return f"Matrimonio de {self.esposo} y {self.esposa}"

class Entierro(models.Model):
    
    entierro_id = models.AutoField(primary_key=True)
    entierro_idno = models.CharField(max_length=50, null=True, blank=True)
    
    acta_entierro = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='acta_entierro', null=True)
    
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='entierros')
    persona_import_id = models.CharField(max_length=100, null=True, blank=True)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='entierros_como_lugar', blank=True, null=True)
    doctrina = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='entierros_como_doctrina', blank=True, null=True)
    fecha = models.DateField(blank=True, help_text="Fecha normalizada del documento")
    notas_fecha = models.CharField(max_length=100, blank=True, null=True, help_text="Fechas incompletas, incorrectas o anotaciones.")
    lugar_declaracion = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='entierros_como_declaracion', null=True)
    legitimidad_difunto = models.CharField(max_length=50, null=True)
    estado_difunto = models.CharField(max_length=50, null=True)
    
    padre = models.ForeignKey(Persona, related_name='padre_difunto', on_delete=models.CASCADE, null=True)
    padre_import_id = models.CharField(max_length=100, null=True, blank=True)
    madre = models.ForeignKey(Persona, related_name='madre_difunto', on_delete=models.CASCADE, null=True)
    madre_import_id  = models.CharField(max_length=100, null=True, blank=True)
    conyuge = models.ForeignKey(Persona, related_name='conyuge_difunto', on_delete=models.CASCADE, null=True)
    conyuge_import_id = models.CharField(max_length=100, null=True, blank=True)
    conyuge_sobrevive = models.CharField(max_length=10, null=True, blank=True)
    tipo_de_entierro = models.CharField(max_length=50, blank=True, null=True)
    
    causa_fallecimiento = models.CharField(max_length=100, null=True, blank=True)
    auxilio_espiritual = models.CharField(max_length=100, null=True, blank=True)
    
    denunciantes = models.ManyToManyField(Persona, related_name='entierros_denunciante')

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.entierro_id:
            self.entierro_idno = f"ent-{str(self.entierro_id).zfill(6)}"
        super(Entierro, self).save(*args, **kwargs)
        if not self.entierro_id: 
            self.entierro_idno = f"ent-{str(self.entierro_id).zfill(6)}"
            super(Entierro, self).save(*args, **kwargs)
        
        
        
        if self.legitimidad_difunto == 'desconocida' or self.legitimidad_difunto == None:
            relationship_type_difunto = "hijo"
        else:
            logger.debug(f"Legitimidad of {self.persona}: {self.legitimidad_difunto}")
            relationship_type_difunto = self.legitimidad_difunto
            
        
        if self.persona and self.padre:
            Relationship.objects.update_or_create(
                left_person=self.persona,
                right_person=self.padre,
                defaults={'relationship_type': relationship_type_difunto}
            )
            Relationship.objects.update_or_create(
                left_person=self.padre,  
                right_person=self.persona,
                defaults={'relationship_type': 'padre'}
            )
        if self.persona and self.madre:
            Relationship.objects.update_or_create(
                left_person=self.persona, 
                right_person=self.madre,
                defaults={'relationship_type': relationship_type_difunto}
            )
            Relationship.objects.update_or_create(
                left_person=self.madre, 
                right_person=self.persona,
                defaults={'relationship_type': 'madre'}
            )
        
        if self.persona and self.conyuge:
            Relationship.objects.update_or_create(
                left_person=self.persona,
                right_person=self.conyuge,
                defaults={'relationship_type': 'casado'}
            )

    def __str__(self) -> str:
        return str(self.persona)
