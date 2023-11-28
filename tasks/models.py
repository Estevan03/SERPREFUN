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
    
# models.py
class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - Cantidad: {self.quantity}"

class ShoppingCart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='CartItem')

    def __str__(self):
        return f"Carrito de {self.user.username}"
