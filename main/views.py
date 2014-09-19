from django.template import RequestContext
from django.shortcuts import render_to_response
from Sitio_Libros.main.models import Libro

def main_page(request):
    list_libros=Libro.objects.all()[:10]
    return render_to_response('main_page.html',RequestContext(request,locals()))


    
            
            

    
    
    
    
    
    
    
    
    
    
    
    
    
