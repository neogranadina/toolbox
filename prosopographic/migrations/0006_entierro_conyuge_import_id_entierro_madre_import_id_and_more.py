# Generated by Django 5.0.2 on 2024-02-14 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosopographic', '0005_alter_historicallugar_tipo_alter_lugar_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='entierro',
            name='conyuge_import_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='entierro',
            name='madre_import_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='entierro',
            name='padre_import_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='entierro',
            name='persona_import_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalentierro',
            name='conyuge_import_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalentierro',
            name='madre_import_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalentierro',
            name='padre_import_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalentierro',
            name='persona_import_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalpersona',
            name='persona_import_identifier',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='persona_import_identifier',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]