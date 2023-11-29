# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Task, CustomUser, Product, Service

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