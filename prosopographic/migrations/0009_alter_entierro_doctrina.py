# Generated by Django 5.0.2 on 2024-04-17 10:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosopographic', '0008_alter_entierro_auxilio_espiritual_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entierro',
            name='doctrina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entierros_como_doctrina', to='prosopographic.lugar'),
        ),
    ]