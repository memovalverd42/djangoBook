"""
    Archivo para configurar los sitemaps de la aplicación

    Los sitemaps son archivos que se utilizan 
    para informar a los motores de búsqueda sobre el contenido
    disponible en un sitio web y para proporcionar información
    adicional que pueda ser útil para la indexación del sitio.
"""

from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    """Clase para crear sitemap de los posts del blog"""

    changefreq = 'weekly' # Frecuencia con la que se actualizará
    priority   = 0.9     

    def items(self):
        '''Metodo que retorna todos los Posts publicados'''
        return Post.published.all()

    def lastmod(self, item):
        '''
            Metodo que devuelve la fecha de última 
            modificación de cada post
        '''
        return item.updated