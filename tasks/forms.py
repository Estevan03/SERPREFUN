# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
      
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=CustomUser.ROLES, initial='cliente')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']

class UserPermissionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['is_superuser', 'is_staff']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price']  # Ajusta los campos según tu modelo

    # Puedes agregar más personalización del formulario aquí si es necesario
    
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_completo', 'tipo_documento', 'numero_documento', 'correo_electronico', 'numero_celular', 'direccion']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['full_name', 'document_type', 'document_number', 'email', 'phone_number', 'address', 'service']
        
class ShoppingCartForm(forms.Form):
    # Puedes agregar más campos según tus necesidades
    direccion_envio = forms.CharField(label='Dirección de Envío', max_length=255)
    comentario = forms.CharField(label='Comentario', widget=forms.Textarea, required=False)