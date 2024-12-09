# Generated by Django 5.1.3 on 2024-11-23 00:23

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_pacientes_telefone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pacientes',
            name='email',
        ),
        migrations.RemoveField(
            model_name='pacientes',
            name='id',
        ),
        migrations.AddField(
            model_name='pacientes',
            name='user_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paciente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pacientes',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='consultas',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='consultas',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='consultas',
            name='status',
            field=models.CharField(choices=[('agendada', 'Agendada'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')], default='agendada', max_length=20),
        ),
        migrations.AlterField(
            model_name='pacientes',
            name='cpf',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^\\d{11}$', message='CPF deve conter 11 dígitos.')]),
        ),
        migrations.AlterField(
            model_name='pacientes',
            name='historico_medico',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pacientes',
            name='telefone',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', message='Número de telefone inválido.')]),
        ),
    ]
