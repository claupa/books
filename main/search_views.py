from django.template import RequestContext
from Sitio_Libros.main.models import Libro
from django.shortcuts import render_to_response
from Sitio_Libros.main.forms import BuscarForm
from django.contrib.auth.decorators import login_required

@login_required
def book_search(request):
    if request.method=='POST':
        form=BuscarForm(request.POST)
        if form.is_valid():            
            titulo = form.cleaned_data['titulo']
            autor = form.cleaned_data['autor']
            books = Libro.objects.filter(titulo__icontains=titulo,autor__icontains=autor)
            variables = RequestContext(request, {'list_libros': books})
            return render_to_response('Search/search_results.html',variables)       
    else:
        form = BuscarForm()
    variables = RequestContext(request, {'form': form})             
    return render_to_response('Search/search.html',variables)    
    
