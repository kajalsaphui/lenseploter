from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class Userform(forms.Form):
    username= forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'placeholder':'Enter your first name'}))
    email= forms.CharField(max_length=100,
                           widget= forms.EmailInput
                           (attrs={'placeholder':'Enter your email'}))
    phonenumber= forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'placeholder':'(xxx)xxx-xxxx'}))