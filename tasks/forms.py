from django.forms import ModelForm
from .models import Task
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role',)

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']