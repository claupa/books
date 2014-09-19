# -*- coding: utf8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from Sitio_Libros.main.models import Persona, Persona_tiene_Libros,Proceso_Prestamo, Mensaje,Libro,Mensajes
from Sitio_Libros.main.forms import Crear_Mensaje
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.contrib.auth.decorators import login_required

@login_required
def detalles_mensaje(request,offset):    
    men=Mensajes.objects.get(id=offset)
    if men.de_quien.username==request.user.username:
        de=men.para_quien.duenno.username
    else:
        de=men.de_quien.username
    asunto=men.get_asunto_display()
    cuerpo=men.cuerpo
    id=men.id
    return render_to_response('Message_Manager/detalles_mensajes.html',RequestContext(request,locals()))

@login_required
def confirmacion(request,offset):
    mensaje=Mensajes.objects.get(id=offset)
    mensaje.delete()
    proc=Proceso_Prestamo.objects.get(pers_solic=mensaje.de_quien,duenno_libro=mensaje.para_quien)
    if proc.estado=='A':
        return __confirmacion_prestamo(proc)
    else:
        if proc.estado=='C':
            return __confirmacion_devolucion(proc)
    return HttpResponseRedirect('/')

def __confirmacion_prestamo(proceso):
    proceso.estado='P'
#   # proceso.fecha_fin_prest+=30
    proceso.save()
    return HttpResponseRedirect('/mensajes/')

def __confirmacion_devolucion(proceso):
    proceso.delete()
    if proceso.fecha_fin_prest<date.today():
        proceso.pers_solic.reputacion+=2
    else:
        if proceso.fecha_fin_prest==date.today():
            proceso.pers_solic.reputacion+=1
        else:
            proceso.pers_solic.reputacion-=1            
    return HttpResponseRedirect('/mensajes/')

@login_required
def ver_mensajes(request):
    user=Persona.objects.get(username=request.user.username)
    duenno_libros=Persona_tiene_Libros.objects.filter(duenno=user)                                                                             
    solicitudes=DameSolicitudes(user,duenno_libros)
    prestamos,devoluciones= DameMensajes(user,duenno_libros)   
    variables= RequestContext(request,locals())
    return render_to_response('Message_Manager/mensajes.html',variables)

def DameSolicitudes(user,duenno_libros):
    solicitudes=[]
    for i in duenno_libros:
        solXlibro=Proceso_Prestamo.objects.filter(duenno_libro=i)
        for j in solXlibro:
            if j.estado=='S' or j.estado=='Solicitado':
                solicitudes.append(j)
    return solicitudes

def DameMensajes(user,duenno_libros):
    prestamos=Mensajes.objects.filter(asunto='1',de_quien=user)
    devoluciones=[]
    for i in duenno_libros:
        devoluciones.extend(Mensajes.objects.filter(asunto='2',para_quien=i))
    return prestamos,devoluciones

def DamePrestamo(user,duenno_libros):
    prestamos=[]    
    for i in duenno_libros:
        solXlibro=Proceso_Prestamo.objects.filter(duenno_libro=i)
        for j in solXlibro: 
            if j.estado=='A' or j.estado=='Confirmacion Prestado':
                prestamos.append(Mensaje.objects.get(id_prestamo=j))
    return prestamos

def DameDevolucion(user,duenno_libros):
    devoluciones=[]
    for i in duenno_libros:
        solXlibro=Proceso_Prestamo.objects.filter(duenno_libro=i)
        for j in solXlibro: 
            if j.estado=='C' or j.estado=='Concluido':
                devoluciones.append(Mensaje.objects.get(id_prestamo=j))
    return devoluciones

#@login_required
#def visto(request,offset):
#    try:
#        mensaje=Mensaje.objects.get(id=offset)
#        mensaje.visto=1
#        mensaje.save()
#    except ObjectDoesNotExist:
#        return HttpResponseRedirect('/')
#    return HttpResponseRedirect('/ver_detalles/')    
        
@login_required        
def ignorar(request,offset):
    try:
        Proceso_Prestamo.objects.get(id=offset)           
    except ObjectDoesNotExist:
        return render_to_response('Message_Manager/mensajes.html',RequestContext(request,{'text':'No puede ignorar una solicitud que no existe.'}))
    proceso=Proceso_Prestamo.objects.get(id=offset)
    if proceso.estado=='S':
        proceso.delete()
    return HttpResponseRedirect('/mensajes/')






@login_required
def crear_mensaje(request):
    if request.method=='POST':
        form=Crear_Mensaje(request.POST)
        if form.is_valid():
            text=''
            libro,estado,duenno,pers_solic=__init(form,request.user)
#            try:
            duenno_de=Persona_tiene_Libros.objects.get(duenno=duenno,libro=libro)
            proc= Proceso_Prestamo.objects.get(duenno_libro=duenno_de,pers_solic=pers_solic)
            if estado=='1' and proc.estado==u'S':
                proc.estado=u'A' 
                proc.save()
            else:
                if estado=='2' and proc.estado==u'P':
                    proc.estado=u'C'
                    proc.save()                              
                                  
#            except ObjectDoesNotExist:             
#                text='1'
#                output='No es posible crear ese mensaje. Revise el usuario al que se lo manda y el libro.'
#                variables=RequestContext(request,{'text':text,'output':output})
#                return render_to_response('Message_Manager/crear_mensaje.html',variables)
            mensaje,created=Mensajes.objects.get_or_create(visto=0,de_quien=pers_solic,para_quien=duenno_de,defaults={'cuerpo':form.cleaned_data['body']})
            if created:
                mensaje.asunto=estado
                mensaje.save()
                return HttpResponseRedirect('/')
            else:
                text='1'
                output='Este mensaje ya existe.'                        
                variables=RequestContext(request,{'text':text,'output':output})
                return render_to_response('Message_Manager/crear_mensaje.html',variables)
    else:
        form=Crear_Mensaje()
    text=''
    variables=RequestContext(request,locals())
    return render_to_response('Message_Manager/crear_mensaje.html',variables)
            
def __init(form,user):
    tipo=form.cleaned_data['asunto']  
    libro=Libro.objects.get(titulo=form.cleaned_data['libro'])
    estado='1'
    pers_solic=Persona.objects.get(username=form.cleaned_data['usuarios'])            
    duenno=Persona.objects.get(username=user.username)
    if tipo==u'2':                         
        temp=duenno
        duenno=pers_solic           
        pers_solic=temp
        estado='2'
    return libro,estado,duenno,pers_solic   

                                  
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            