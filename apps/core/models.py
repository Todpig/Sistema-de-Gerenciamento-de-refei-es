import uuid
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


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
    likes = models.IntegerField("Curtidas", default=0, null=True, blank=True)
    image = models.ImageField("Imagem", upload_to=get_file_path, null=True)
    snack_to_day = models.BooleanField("Refeição do dia", default=False)
    type = models.CharField("Tipo", max_length=15, choices=type_choices)
    active = models.BooleanField("Ativo", default=True, null=True, blank=True)

class RequestSnack(models.Model):
    snack_types = Snack.type_choices

    student_name = models.CharField("Nome do aluno", max_length=150)
    student_registration = models.CharField("Matrícula do aluno", max_length=150)
    data = models.DateField("Data")
    justification = models.TextField("Justificativa", max_length=300)
    status = models.BooleanField("Situação", default=False, blank=True, null=True)
    type = models.CharField("Tipo", max_length=15, choices=snack_types)


# class UserManager(BaseUserManager):

#     def create_user(self, username,email,password=None,first_name='',last_name=''):
#         if username is None:
#             raise TypeError('Usuário deve informar o nome')
#         if email is None:
#             raise TypeError('Users deve informar o Email')
    
#         user = self.model(username=username,email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, username, email, password=None):
#         if password is None:
#             raise TypeError('Password should not be none')

#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()

#         return user

# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField('Nome Usuário',max_length=255, db_index=True)
#     email = models.EmailField(max_length=255, unique=True, db_index=True)
#     is_staff = models.BooleanField(default=False)
#     is_anonymous = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     coordinator = models.BooleanField(default=False)
#     chef = models.BooleanField(default=False)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     objects = UserManager()

#     def __str__(self):
#         return self.email

#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         }

#     def get_token_access(self):
#         refresh = RefreshToken.for_user(self)
#         return str(refresh.access_token)

#     class Meta:
#         verbose_name = "Usuário"
