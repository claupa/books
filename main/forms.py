# -*- coding: utf8 -*-

import re
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from Sitio_Libros.main.models import Persona,Libro, Mensajes
from django.contrib.auth.models import User
from django.forms import ModelForm
#from django.contrib.auth.decorators import user_passes_test
#from django.template.defaultfilters import default

class userForm(ModelForm):
    class Meta:
        model =Persona
        exclude=('username','password','reputacion',)
        
class bookForm(ModelForm):
    class Meta:
        model =Libro

class addForm(ModelForm):
    class Meta:
        model =Libro  
           
    count=forms.IntegerField(label='Cantidad de Copias', required=False,initial=1)   
    resumen=forms.CharField(required=False,label='Resumen',widget=forms.Textarea)       
        
class FriendInviteForm(forms.Form):
    name = forms.CharField(label='Nombre')
    email = forms.EmailField(label='Correo ')

class Change_Password(forms.Form):
    old_pass= forms.CharField(max_length=50,label='Contraseña Actual',widget=forms.PasswordInput(),error_messages={'required': 'Este campo es obligatorio.'})    
    new_password = forms.CharField(max_length=50,label='Nueva Contraseña',widget=forms.PasswordInput(),error_messages={'required': 'Este campo es obligatorio.'})
    password2 = forms.CharField(max_length=50,label='Confirme Contraseña',widget=forms.PasswordInput(),error_messages={'required': 'Este campo es obligatorio.'})
    __user=User()   
     
    def __init__(self,request):
        forms.Form.__init__(self,request.POST)
        self.__user= request.user        
        
    def clean_old_pass(self):
        if 'old_pass' in self.cleaned_data:
            old_pass=self.cleaned_data['old_pass']
            if not self.__user.check_password(old_pass):
                raise forms.ValidationError('Esta contraseña no coincide con la actual.')
    def clean_password2(self):       
        if 'new_password' in self.cleaned_data:
            new_password = self.cleaned_data['new_password']
            password2 = self.cleaned_data['password2']
            if new_password == password2:
                return password2
        raise forms.ValidationError('Las claves no son iguales.') 

class BuscarForm(forms.Form):
    titulo=forms.CharField(max_length=50,label="Título",required=False)
    autor=forms.CharField(max_length=50,label="Autor",required=False)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=50,error_messages={'required': 'Este campo es obligatorio.'})    
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput(),error_messages={'required': 'Este campo es obligatorio.'})
    password2 = forms.CharField(label='Confirme Contraseña',widget=forms.PasswordInput(),error_messages={'required': 'Este campo es obligatorio.'})
    email = forms.EmailField(label='Correo',error_messages={'required': 'Este campo es obligatorio.'})    
    nombre=forms.CharField(max_length=50,error_messages={'required': 'Este campo es obligatorio.'},label='Nombre')
    apellido1=forms.CharField(max_length=50,error_messages={'required': 'Este campo es obligatorio.'},label='1er apellido')
    apellido2=forms.CharField(max_length=50,error_messages={'required': 'Este campo es obligatorio.'},label='2do apellido')
    Sexo=((u'M',u'Mujer'),(u'H',u'Hombre'),)
    sexo=forms.ChoiceField(choices=Sexo,label='Sexo')        
    direccion=forms.CharField(max_length=256, required=False,label='Dirección',help_text='Ejemplo: Calle:0 e/0 y 0 apto 0, Plaza de la Revolución, La Habana')
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Las claves no son iguales.')        
    def clean_username(self):
        username = self.cleaned_data['username']        
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('El nombre de usuario solo puede contener caracteres alfanumericos y el underscore.')
        try:
            Persona.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('El nombre de usuario ya existe.')
    def clean_direccion(self):
        if 'direccion' in self.cleaned_data:
            direccion=self.cleaned_data['direccion']
            if not re.search(r'^Calle:(\d{1,3})|[A-Z a-z]+ e/(\d{1,3})|[A-Z a-z]+ y (\d{1,3})|[A-Z a-z]+ apto (\d{1,3})|[A-Z a-z]+, [A-Z a-z]+, [A-Z a-z]+ $', direccion):
                raise forms.ValidationError('Introdujo mal la dirección.')
            return direccion
        raise forms.ValidationError('No se introdujo ninguna dirección.')
    def clean_nombre(self):
        if 'nombre' in self.cleaned_data:
            nombre = self.cleaned_data['nombre']
            if not re.search(r'^[A-Z a-z]+$', nombre):
                raise forms.ValidationError('Introdujo mal el nombre')
            return nombre
        raise forms.ValidationError('No se introdujo el nombre')
    def clean_apellido1(self):
        if 'apellido1' in self.cleaned_data:
            apellido1 = self.cleaned_data['apellido1']
            if not re.search(r'^[A-Z a-z]+$', apellido1):
                raise forms.ValidationError('Introdujo mal el primer apellido')
            return apellido1
        raise forms.ValidationError('No se introdujo el primer apellido')
    def clean_apellido2(self):
        if 'apellido2' in self.cleaned_data:
            apellido2 = self.cleaned_data['apellido2']
            if not re.search(r'^[A-Z a-z]+$', apellido2):
                raise forms.ValidationError('Introdujo mal el segundo apellido')
            return apellido2
        raise forms.ValidationError('No se introdujo el segundo apellido')
    
class Send_Mail(forms.Form):
    correo=forms.EmailField(label='Correo del Invitado:')    
   
class Solicitud_Libro_Directa(forms.Form):
    username=forms.CharField(label='Peticion a:',max_length=50,error_messages={'required': 'Este campo es obligatorio'})
    libro_code=forms.IntegerField(label='Codigo del Libro',error_messages={'required': 'Este campo es obligatorio'}) 

class Crear_Mensaje(forms.Form):       
    Asuntos=((u'1',u'Confirmación de Préstamo'),(u'2',u'Confirmación de Devolución'))
    asunto=forms.ChoiceField(choices=Asuntos,label='Asunto:')    
    usuarios=forms.CharField(max_length=50,label='Mandar a:')
    libro=forms.CharField(max_length=100,label='Sobre el Libro:')
    body=forms.CharField(widget=forms.Textarea, label='Mensaje:', required=False)  
    def clean_usuarios(self):
        if 'usuarios' in self.cleaned_data:
            username=self.cleaned_data['usuarios']
            try:
                Persona.objects.get(username=username)
                return username
            except ObjectDoesNotExist:
                raise forms.ValidationError('Ese usuario no existe.')
    def clean_libro(self):
        if 'libro' in self.cleaned_data:
            libro=self.cleaned_data['libro']
            try:
                Libro.objects.get(titulo=libro)
                return libro
            except ObjectDoesNotExist:
                raise forms.ValidationError('Ese libro no existe.')             
        