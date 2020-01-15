from django.forms import ModelForm
from .models import Product
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'price', 'photo', 'status']

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'
