from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.conf import settings


PLACE_TYPE_CHOICES = (
        ('ciudad', 'Ciudad'),
        ('pueblo', 'Pueblo'),
        ('estado', 'Estado'),
        ('gobernacion', 'Gobernación'),
        ('pais', 'País'),
        ('provincia', 'Provincia'),
        ('villa', 'Villa'),
        ('real', 'Real de Minas'),
        ('parroquia', 'Parroquia'),
        ('fuerte', 'Fuerte')
    )

###############
# Lugares
###############

class Lugar(models.Model):
    
    lugar_id = models.AutoField(primary_key=True)
    nombre_lugar = models.CharField(max_length=255)
    es_parte_de = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    tipo = models.CharField(max_length=50, choices=PLACE_TYPE_CHOICES)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='created_by', blank=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='updated_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        
        return f"{self.nombre_lugar} ({self.tipo})"

class PlaceHistorical(models.Model):
    
    registro_id = models.AutoField(primary_key=True)
    
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='historical_names')
    nombre_original = models.CharField(max_length=255, default="Legacy")
    tipo_original = models.CharField(max_length=255, default="Legacy")
    otro_nombre = models.CharField(max_length=255, help_text="¿Es un nombre diferente?", null=True, blank=True)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField(null=True, blank=True)
    otro_tipo = models.CharField(max_length=50, choices=PLACE_TYPE_CHOICES, help_text="¿Es un tipo diferente?", null=True, blank=True)
    narrativa = models.TextField(null=True, blank=True)
    
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.otro_nombre} | {self.lugar.nombre_lugar} ({self.fecha_inicial} - {self.fecha_final or 'Present'})"