from django.db import models

# Create your models here.
class CaObject(models.Model):
    object_id = models.IntegerField(primary_key=True)

    class Meta:
        app_label = 'hello'
        managed = False
        db_table = 'ca_objects'  # Make sure this matches your actual table name

    def __str__(self):
        return str(self.object_id)
    
class CaEntityLabel(models.Model):
    label_id = models.AutoField(primary_key=True)
    entity_id = models.IntegerField()
    locale_id = models.SmallIntegerField()
    type_id = models.IntegerField(null=True)
    displayname = models.CharField(max_length=512)
    forename = models.CharField(max_length=100)
    other_forenames = models.CharField(max_length=100, null=True)
    middlename = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=512)
    prefix = models.CharField(max_length=100, null=True)
    suffix = models.CharField(max_length=100, null=True)
    name_sort = models.CharField(max_length=512)
    source_info = models.TextField()  # longtext in MySQL
    is_preferred = models.PositiveSmallIntegerField()  # tinyint in MySQL
    sdatetime = models.DecimalField(max_digits=30, decimal_places=20, null=True)
    edatetime = models.DecimalField(max_digits=30, decimal_places=20, null=True)
    access = models.PositiveSmallIntegerField(default=0)
    checked = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        app_label = 'hello'
        managed = False
        db_table = 'ca_entity_labels'
        
    def __str__(self):
        return f"{self.forename} {self.middlename} {self.surname} ({self.displayname})"
        
    