
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Consultas

@shared_task
def enviar_lembrete_consultas():
    agora = datetime.now()
    limite = agora + timedelta(days=1)

    consultas = Consultas.objects.filter(data_hora__range=(agora, limite), status='agendada')
    for consulta in consultas:
        send_mail(
            'Lembrete de Consulta',
            f'Sua consulta está agendada para {consulta.data_hora}.',
            'noreply@seusite.com',
            [consulta.paciente.email],
        )
