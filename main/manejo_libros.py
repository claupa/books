from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from Sitio_Libros.main.models import Persona, Persona_tiene_Libros,Proceso_Prestamo, Libro
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.contrib.auth.decorators import login_required
from Sitio_Libros.main.forms import bookForm

@login_required
def consultar_deudas(request):
    user=Persona.objects.get(username=request.user.username)
    relac=Proceso_Prestamo.objects.filter(pers_solic=user)
    libros_debe=[]
    for i in relac:
        if i.estado==u'P' or i.estado==u'Prestado':
            libros_debe.append(i)
    return render_to_response('Book_Manager/deudas.html',RequestContext(request,{'titulos':libros_debe,'duedas':relac,'count':libros_debe.__len__()}))

@login_required
def detalles_deuda(request,offset):
    try:
        proc=Proceso_Prestamo.objects.get(id=offset)
        if proc.estado=='P' and proc.pers_solic==Persona.objects.get(username=request.user.username):
            text=''
        else:
            text='Esta accediendo a un lugar equivocado.'
    except ObjectDoesNotExist:
        text='Esta muy mal.'
    variables=RequestContext(request,locals())
    return render_to_response('Book_Manager/detalles_deudas.html',variables)

@login_required
def ver_prestado(request):
    user=Persona.objects.get(username=request.user.username)
    duenno_de=Persona_tiene_Libros.objects.filter(duenno=user)
    prestados=[]
    for i in duenno_de:
        procesos=Proceso_Prestamo.objects.filter(duenno_libro=i)
        for j in procesos:
            if j.estado=='P':
                prestados.append(j)
    variables=RequestContext(request,{'prestados':prestados,'count':prestados.__len__()})
    return render_to_response('Book_Manager/ver_prestados.html',variables)

@login_required
def detalles_prestados(request,offset):
    try:
        proc=Proceso_Prestamo.objects.get(id=offset)
        if proc.estado=='P' and proc.duenno_libro.duenno==Persona.objects.get(username=request.user.username):
            text=''
        else:
            text='Esta accediendo a un lugar equivocado.'
    except ObjectDoesNotExist:
        text='Esta muy mal.'
    variables=RequestContext(request,locals())
    return render_to_response('Book_Manager/detalles_prestados.html',variables)

@login_required
def prestamo_hecho(request,offset):
    try:
        proceso=Proceso_Prestamo.objects.get(id=offset)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/')
    if proceso.estado=='S':
        proceso.estado='P'
        proceso.fecha_inic_prest=date.today()
        proceso.fecha_fin_prest=date.today()+30
        proceso.save()
    return HttpResponseRedirect('/')

@login_required
def ver_libros(request,username):
    user = Persona.objects.get(username=request.user.username)
    user_books = Persona_tiene_Libros.objects.filter(duenno=user)
    users_books_all = []
    for i in user_books:
        users_books_all.append(Libro.objects.get(id=i.libro.id))
    return render_to_response('Book_Manager/ver_libros.html',RequestContext(request,{'titulos':users_books_all,'count':users_books_all.__len__()}))


def editar_libro(request, offset):
    libro=Libro.objects.get(id=offset)
    if request.method=='POST':        
        form=bookForm(request.POST)
        if form.is_valid():            
            datos_libro=form.save(commit=False)
            libro.titulo = datos_libro.titulo
            libro.autor = datos_libro.autor
            libro.numero_de_edicion= datos_libro.numero_de_edicion
            libro.anno_de_publicacion=datos_libro.anno_de_publicacion
            libro.save()
            return HttpResponseRedirect('/')
    else:
        form=bookForm(initial={'titulo':libro.titulo,'autor':libro.autor,'edicion':libro.numero_de_edicion,'publicacion':libro.anno_de_publicacion})
    variables = RequestContext(request, locals())
    return render_to_response('Book_Manager/editar_libro.html',variables)
    
def eliminar_libro(request, offset):
    libro=Libro.objects.get(id=offset)
    libro.delete()
    return HttpResponseRedirect('/')