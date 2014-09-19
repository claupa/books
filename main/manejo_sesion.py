# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from Sitio_Libros.main.models import Invitation, Persona, Persona_tiene_Libros, Libro
from Sitio_Libros.main.forms import FriendInviteForm, Change_Password, RegistrationForm, Send_Mail, userForm
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import django.core.context_processors


@login_required 
def logout_page(request):
    logout(request) 
    return HttpResponseRedirect('/')

@login_required    
def change_password(request):
    if request.method == 'POST':
        form = Change_Password(request)
        if form.is_valid():            
            user = Persona.objects.get(username=request.user.username)  
            user.password = form.cleaned_data['password2']           
            user.save()
            usuario=User.objects.get(username=user.username)
            usuario.set_password(user.password)
            usuario.save()
            return HttpResponseRedirect('/')                               
    else:      
        form = Change_Password(request)
    variables = RequestContext(request, {'form': form})    
    return render_to_response('registration/change_password.html', variables) 

def friend_accept(request, code):
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('/register/')

@login_required
def user_page(request,username):
    persona=Persona.objects.get(username=request.user.username)
    if request.method=='POST':        
        form=userForm(request.POST)
        if form.is_valid():            
            datos_persona=form.save(commit=False)
            persona.nombre = datos_persona.nombre
            persona.apellido1 = datos_persona.apellido1
            persona.apellido2 = datos_persona.apellido2
            persona.sexo = datos_persona.sexo
            persona.direccion = datos_persona.direccion
            persona.email = datos_persona.email
            persona.save()
            return HttpResponseRedirect('/')
    else:
        form=userForm(initial={'nombre':persona.nombre,'apellido1':persona.apellido1,'apellido2':persona.apellido2,'email':persona.email,'sexo':persona.sexo,'reputacion':persona.reputacion,'direccion':persona.direccion})
    variables = RequestContext(request, locals())
    return render_to_response('registration/user_page.html',variables)

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():             
            user = Persona(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'], nombre=form.cleaned_data['nombre'], apellido1=form.cleaned_data['apellido1'], apellido2=form.cleaned_data['apellido2'], sexo=form.cleaned_data['sexo'], direccion=form.cleaned_data['direccion'])
            user.reputacion = 0         
            user.save()
            User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            return HttpResponseRedirect('/register/success')
        if 'invitation' in request.session:
            invitation = Invitation.objects.get(id=request.session['invitation']) 
            invitation.delete()
            del request.session['invitation']
            return HttpResponseRedirect('/register/success/') 
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables) 

@login_required
def send_inv(request):
    if request.method == 'POST':
        form = Send_Mail(request.POST)
        if form.is_valid():
            usuario = request.user.username                                       
            person = Persona.objects.get(username=usuario)
            name = person.nombre + ' ' + person.apellido1 + ' ' + person.apellido2
            mensaje = 'Usted ha recibido una invitacion al sitio de los libros. Su codigo de registro es '
            try:
                send_mail('Invitacion', mensaje, name, form.cleaned_data['correo'])
                return render_to_response('envio_satisfactorio.html', RequestContext(request, {'form':form})) 
            except:
                raise Http404('Problema con el envio')         
    else:
        form = Send_Mail()
    return render_to_response('registration/enviar_invitacion.html', RequestContext(request, {'form':form}))

@login_required
def friend_invite(request):
    if request.method == 'POST':
        form = FriendInviteForm(request.POST)
        if form.is_valid():
            invitation = Invitation(name = form.cleaned_data['name'], email = form.cleaned_data['email'], code = User.objects.make_random_password(20),sender = request.user)
            invitation.save()
            invitation.send()            
#        try:
#            invitation.send()
#            request.user.message_set.create(message='Se envió una invitación a %s.' % invitation.email)
#        except:
#            request.user.message_set.create(message='Hubo un error mientras se mandaba la invitacion.')
            return HttpResponseRedirect('/send_inv/')
    else:
        form = FriendInviteForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/friend_invite.html', variables)
