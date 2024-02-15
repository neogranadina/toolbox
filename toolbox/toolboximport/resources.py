from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from prosopographic.models import (Archivo, Documento, Lugar, Persona,
                                   Bautismo, Matrimonio, Entierro)


class ArchivoResource(resources.ModelResource):
    archivo_id = Field(attribute='archivo_id', column_name='id', saves_null_values=False)
    archivo_nombre = Field(attribute='archivo_nombre', column_name='archivo_nombre')
    archivo_sigla = Field(attribute='archivo_sigla', column_name='archivo_sigla')

    class Meta:
        model = Archivo
        import_id_fields = ['archivo_id'] 
        fields = ('archivo_id', 'archivo_nombre', 'archivo_sigla') 
        skip_unchanged = True
        report_skipped = False


class DocumentoResource(resources.ModelResource):
    documento_id = Field(attribute='documento_id', column_name='id', saves_null_values=False)
    archivo = Field(
        column_name='archivo',
        attribute='archivo',
        widget=ForeignKeyWidget(Archivo, 'archivo_sigla')
    )
    
    class Meta:
        model = Documento
        import_id_fields = ['documento_id']
        fields = ('documento_id', 'archivo', 'unidad_documental', 'identificador', 'titulo_documento', 'folios', 'rango_imagenes', 'notas', 'condicion_documento')
        skip_unchanged = True
        report_skipped = False
    
class LugarResource(resources.ModelResource):
    lugar_id = Field(attribute='lugar_id', column_name='id', saves_null_values=False)
    
    class Meta:
        model = Lugar
        import_id_fields = ['lugar_id']
        fields = ('lugar_id', 'nombre', 'otros_nombres', 'tipo', 'lat', 'lon')
        skip_unchanged = True
        report_skipped = False    

class PersonaResource(resources.ModelResource):
    persona_id = Field(attribute='persona_id', column_name='id', saves_null_values=False)
    vecindad = Field(
        column_name='vecindad',
        attribute='vecindad',
        widget=ForeignKeyWidget(Lugar, 'nombre')
    )
    
    class Meta:
        model = Persona
        import_id_fields = ['persona_id']
        fields = ('persona_id', 'nombre', 'apellidos', 'nombre_completo', 'fecha_nacimiento', 'notas_fecha_nacimiento', 'fecha_defuncion', 'notas_fecha_defuncion', 'lugar_nacimiento', 'vecindad', 'condicion')
        skip_unchanged = True
        report_skipped = False

class EntierroResource(resources.ModelResource):
    entierro_id = Field(attribute='entierro_id', column_name='id', saves_null_values=False)
    persona = Field(
        column_name='persona',
        attribute='persona',
        widget=ForeignKeyWidget(Persona, 'nombre_completo')
    )
    
    padre = Field(
        column_name='padre',
        attribute='padre',
        widget=ForeignKeyWidget(Persona, 'nombre_completo')
    )
    
    madre = Field(
        column_name='madre',
        attribute='madre',
        widget=ForeignKeyWidget(Persona, 'nombre_completo')
    )
    
    conyuge = Field(
        column_name='conyuge',
        attribute='conyuge',
        widget=ForeignKeyWidget(Persona, 'nombre_completo')
    )
    
    acta_entierro = Field(
        column_name='acta_entierro',
        attribute='acta_entierro',
        widget=ForeignKeyWidget(Documento, 'identificador')
    )
    
    lugar = Field(
        column_name='lugar',
        attribute='lugar',
        widget=ForeignKeyWidget(Lugar, 'nombre')
    )
    
    doctrina = Field(
        column_name='doctrina',
        attribute='doctrina',
        widget=ForeignKeyWidget(Lugar, 'nombre')
    )
    
    lugar_declaracion = Field(
        column_name='lugar_declaracion',
        attribute='lugar_declaracion',
        widget=ForeignKeyWidget(Lugar, 'nombre')
    )
    
    class Meta:
        model = Entierro
        import_id_fields = ['entierro_id']
        fields = ('acta_entierro', 'persona', 'lugar', 'doctrina', 'fecha', 'notas_fecha', 'lugar_declaracion', 'legitimidad_difunto', 'estado_difunto', 'padre', 'madre', 'conyuge', 'conyuge_sobrevive', 'tipo_de_entierro', 'causa_fallecimiento', 'auxilio_espiritual')
        skip_unchanged = True
        report_skipped = False