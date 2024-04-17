# Generated by Django 5.0 on 2024-02-12 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosopographic', '0002_bautismo_notas_fecha_entierro_notas_fecha_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bautismo',
            old_name='notas_fecha',
            new_name='notas_fecha_bautismo',
        ),
        migrations.RenameField(
            model_name='historicalbautismo',
            old_name='notas_fecha',
            new_name='notas_fecha_bautismo',
        ),
        migrations.RenameField(
            model_name='historicalmatrimonio',
            old_name='notas_fecha',
            new_name='notas_fecha_matrimonio',
        ),
        migrations.RenameField(
            model_name='historicalpersona',
            old_name='notas_fecha',
            new_name='notas_fecha_defuncion',
        ),
        migrations.RenameField(
            model_name='matrimonio',
            old_name='notas_fecha',
            new_name='notas_fecha_matrimonio',
        ),
        migrations.RenameField(
            model_name='persona',
            old_name='notas_fecha',
            new_name='notas_fecha_defuncion',
        ),
        migrations.AddField(
            model_name='historicalpersona',
            name='notas_fecha_nacimiento',
            field=models.CharField(blank=True, help_text='Fechas incompletas, incorrectas o anotaciones.', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='notas_fecha_nacimiento',
            field=models.CharField(blank=True, help_text='Fechas incompletas, incorrectas o anotaciones.', max_length=100, null=True),
        ),
    ]