# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
    
class Persona(models.Model):
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50)    
    email=models.EmailField()
    nombre=models.CharField(max_length=50)
    apellido1=models.CharField(max_length=50)
    apellido2=models.CharField(max_length=50)
    Sexo=((u'M',u'Mujer'),(u'H',u'Hombre'),)
    sexo=models.CharField(max_length=2,choices=Sexo)        
    direccion=models.CharField(max_length=256)
    reputacion=models.IntegerField()  
    def __str__(self):
        return self.username    
        
class Libro(models.Model):
    titulo=models.CharField(max_length=100)
    autor=models.CharField(max_length=100)
    numero_de_edicion=models.IntegerField()  
    anno_de_publicacion=models.DateField()   
    class Meta:        
        ordering=['titulo']
    def __str__(self):
        return '%s,por %s' % (self.titulo, self.autor)
    
class Persona_tiene_Libros(models.Model):
    duenno=models.ForeignKey(Persona)
    libro=models.ForeignKey(Libro)
    count=models.IntegerField()
    resumen=models.TextField(null=True,blank=True)    
    class Meta:
        ordering=['libro']

class Proceso_Prestamo(models.Model):
    duenno_libro=models.ForeignKey(Persona_tiene_Libros)
    pers_solic=models.ForeignKey(Persona)
    Estados_Proceso=((u'P',u'Prestado'),(u'A',u'Confirmacion Prestado'),(u'S',u'Solicitado'),(u'C',u'Concluido'))
    estado=models.CharField(max_length=2,choices=Estados_Proceso)
    fecha_inic_prest=models.DateField(null=True)
    fecha_fin_prest=models.DateField(null=True)
    class Meta:
        ordering=['duenno_libro']
        
class Mensaje(models.Model):
    Asuntos=((u'1',u'Confirmación de Préstamo'),(u'2',u'Confirmación de Devolución'))
    asunto=models.CharField(max_length=100,choices=Asuntos)
    cuerpo=models.TextField(blank=True,null=True)
    visto=models.IntegerField()
    id_prestamo=models.ForeignKey(Proceso_Prestamo)
    

class Mensajes(models.Model):
    Asuntos=((u'1',u'Confirmación de Préstamo'),(u'2',u'Confirmación de Devolución'))
    asunto=models.CharField(max_length=100,choices=Asuntos)
    de_quien=models.ForeignKey(Persona)
    para_quien=models.ForeignKey(Persona_tiene_Libros)
    cuerpo=models.TextField()    
    visto=models.IntegerField()
    
class Invitation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(User)
    def __str__(self):
        return '%s, %s' % (self.sender.username, self.email)
    class Admin:
        pass
    def send(self):
        subject = 'Invitacion para unirse al sitio Libros'
        link = 'http://%s/friend/accept/%s/' % (settings.SITE_HOST,self.code)
        template = get_template('invitation_email.txt')
        context = Context({'name': self.name,'link': link,'sender': self.sender.username,})
        message = template.render(context)
        send_mail(subject, message,settings.DEFAULT_FROM_EMAIL, [self.email])