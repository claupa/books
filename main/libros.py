from Sitio_Libros.main.models import Libro, Persona,Persona_tiene_Libros, Proceso_Prestamo
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from Sitio_Libros.main.forms import addForm
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def latest_books(request):
    list_libros=Libro.objects.all()[:10]
    return render_to_response('Books/latest_books.html',RequestContext(request,locals()))

@login_required
def books_page(request,offset):
    text=''
    try:
        book=Libro.objects.get(id=offset)
        todo=Persona_tiene_Libros.objects.filter(libro=book)
    except ObjectDoesNotExist:
        text='El libro no existe.'
    return render_to_response('Books/books_page.html',RequestContext(request,locals()))

@login_required
def adding_books(request):
    if request.method=='POST':
        form=addForm(request.POST)
        if form.is_valid():            
            libro=form.save(commit=False)   
            try:
                libro=Libro.objects.get(titulo=libro.titulo,autor=libro.autor,numero_de_edicion=libro.numero_de_edicion)
            except ObjectDoesNotExist:
                libro.save()
            user=Persona.objects.get(username=request.user.username)
            libro_de, created=Persona_tiene_Libros.objects.get_or_create(duenno=user,libro=libro,defaults={'count':form.cleaned_data['count'],'resumen':form.cleaned_data['resumen']})                                  
            libro_de.save()
            return HttpResponseRedirect('/add_book/')
    else:
        form=addForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('Books/adding_books.html',variables) 

@login_required
def book_request(request,offset):
    text=''
    try:
        book=Libro.objects.get(id=offset)
        duenno=Persona_tiene_Libros.objects.filter(libro=book)
    except ObjectDoesNotExist:
        text='El libro no existe.'
    return render_to_response('Books/request.html',RequestContext(request,locals()))

@login_required
def solicitud_directa(request,offset):
    duenno=Persona_tiene_Libros.objects.get(id=offset)
    user=Persona.objects.get(username=request.user.username)
    if user==duenno.duenno:
        text='No se puede hacer una solicitud a si mismo.'
        return render_to_response('Books/request.html',RequestContext(request,locals()))        
    try:
        p=Proceso_Prestamo.objects.get(duenno_libro=duenno,pers_solic=user)
        text='Esta solicitud ya se hizo. No puede volverla a hacer.'
    except ObjectDoesNotExist:
        solicitud=Proceso_Prestamo(duenno_libro=duenno,pers_solic=user,estado='S',fecha_inic_prest=date.today(), fecha_fin_prest=date.today())
        solicitud.save() 
        text='1' 
    return render_to_response('Books/request.html',RequestContext(request,locals()))