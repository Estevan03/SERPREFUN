from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

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
        ('cliente', 'Cliente'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='cliente')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    
class ShoppingCart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='CartItem')

    def __str__(self):
        return f"Carrito de {self.user.username}"


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else self.service.name}"

    @property
    def total(self):
        # Lógica para calcular el total
        return self.quantity * self.product.price if self.product else self.quantity * self.service.price

    @total.setter
    def total(self, value):
        # No hacemos nada aquí, ya que el total se calcula automáticamente
        pass
    
class Pedido(models.Model):
    servicio = models.ForeignKey(Service, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=50)
    correo_electronico = models.EmailField()
    numero_celular = models.CharField(max_length=20)
    direccion = models.TextField()
    
    
class ServiceRequest(models.Model):
    full_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50)
    document_number = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    service_id = models.IntegerField()  # Enlazar con el servicio solicitado

    def __str__(self):
        return f"Solicitud de servicio para {self.full_name}"
