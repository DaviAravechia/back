# Generated by Django 5.1.3 on 2024-11-06 00:32

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('data_nascimento', models.DateField()),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(max_length=254)),
                ('historico_medico', models.TextField()),
                ('cpf', models.CharField(max_length=11)),
            ],
        ),
    ]