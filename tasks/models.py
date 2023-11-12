from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import validate_email

# Create your models here.

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username


class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('nuevo_usuario', 'Nuevo Usuario'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='nuevo_usuario')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']