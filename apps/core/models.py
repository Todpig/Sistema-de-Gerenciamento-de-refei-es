import uuid
from django.db import models

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename
class Snack(models.Model):
    type_choices = (
        ("almoço", "almoço"),
        ("janta", "janta"),
    )
    description = models.TextField("Descrição", max_length=255)
    likes = models.IntegerField("Curtidas", default=0)
    image = models.ImageField("Imagem", upload_to=get_file_path, null=True)
    snack_to_day = models.BooleanField("Refeição do dia", default=False)
    type = models.CharField("Tipo", max_length=15, choices=type_choices)
    active = models.BooleanField("Ativo", default=True)

class RequestSnack(models.Model):
    snack_types = Snack.type_choices

    student_name = models.CharField("Nome do aluno", max_length=150)
    student_registration = models.CharField("Matrícula do aluno", max_length=150)
    data = models.DateField("Data")
    justification = models.TextField("Justificativa", max_length=300)
    status = models.BooleanField("Situação", default=False)
    type = models.CharField("Tipo", max_length=15, choices=snack_types)
