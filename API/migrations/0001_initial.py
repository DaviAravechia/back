# Generated by Django 5.1.3 on 2024-11-28 23:39

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=255)),
                ('crm', models.CharField(max_length=20, unique=True)),
                ('telefone', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Médico',
                'verbose_name_plural': 'Médicos',
            },
        ),
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=255)),
                ('data_nascimento', models.DateField()),
                ('telefone', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('historico_medico', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
            },
        ),
        migrations.CreateModel(
            name='Consultas',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('data_hora', models.DateTimeField()),
                ('descricao', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('agendada', 'Agendada'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')], max_length=50)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='API.pacientes')),
            ],
            options={
                'verbose_name': 'Consulta',
                'verbose_name_plural': 'Consultas',
            },
        ),
    ]
