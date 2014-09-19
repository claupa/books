import os.path
from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template
from Sitio_Libros.main.search_views import book_search
from Sitio_Libros.main.libros import books_page, adding_books, book_request,solicitud_directa, latest_books
from Sitio_Libros.main.manejo_sesion import friend_accept ,friend_invite, logout_page,send_inv, register_page,change_password,user_page
from Sitio_Libros.main.manejo_libros import  ver_libros,editar_libro, eliminar_libro,consultar_deudas,  ver_prestado,detalles_deuda,detalles_prestados
from Sitio_Libros.main.manejo_mensajes import ignorar, ver_mensajes, crear_mensaje, detalles_mensaje,confirmacion
from Sitio_Libros.main.views import  main_page


site_media = os.path.join(os.path.dirname(__file__), 'site_media')

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': site_media }), 
    (r'^$', main_page), 
                        
    # Manejo de usuarios #
    (r'^user/(\w+)/$', user_page),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),    
    #(r'^send_inv/$',send_inv),    
    (r'^register/$', register_page),
    (r'^register/success/$', direct_to_template,{ 'template': 'registration/register_success.html' }),
    (r'^change_password/$',change_password),
    (r'^send_inv/$', friend_invite),
    (r'^friend/accept/(\w+)/$', friend_accept),
    # Fin Manejo de usuarios #    
    
    # Libros #
    (r'^book/(\d*)/$',books_page),
    (r'^add_book/$',adding_books),
    (r'^request/(\d*)/$',book_request),
    (r'^latest_books/$',latest_books),
    (r'^solicitud_duenno/(\d*)$',solicitud_directa),
    # Fin Libros #
    
    # Busqueda #
    (r'^buscar/$',book_search),
    # Fin Busqueda #
    
    # Manejo Libros #
    (r'^deudas/$', consultar_deudas),    
    (r'detalles_deuda/(\d*)/', detalles_deuda), 
    (r'^libros_prestados/$',ver_prestado),
    (r'^detalles_prestados/(\d*)/$',detalles_prestados), 
    (r'^libros/(\w+)/$', ver_libros),
    (r'^editar_libro/(\d+)/$', editar_libro),
    (r'^eliminar_libro/(\d+)/$', eliminar_libro),  
    # Fin Manejo Libros #
    
    # Manejo de Mensajes #
    (r'^mensajes/$',ver_mensajes),
    (r'^ignorar/(\d*)/$',ignorar),
    (r'^crear_mensaje/$',crear_mensaje),
    (r'^detalles_mensaje/(\d*)/$',detalles_mensaje),
    (r'^accept/(\d*)/$',confirmacion)
    # Fin Manejo Mensajes #    
)
