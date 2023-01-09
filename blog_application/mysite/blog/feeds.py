'''
    Un feed es un archivo que se utiliza para publicar 
    actualizaciones de un sitio web de manera sindicada
    y que permite a los usuarios suscribirse a ellas
    para recibir notificaciones de las actualizaciones del sitio.
'''

import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LastestPostsFeed(Feed):
    '''Clase para crear feed sobre los posts'''
    titel = 'Mi blog'
    # link generado por la función reverse_lazy() que se genera al
    # terminar de cargar el sitio
    link = reverse_lazy('blog:post_list')
    description = 'Nuevos posts del blog'

    def items(self):
        '''Metodo que retorna 5 de los Posts publicados'''
        return Post.published.all()[:5]
    
    def item_title(self, item):
        '''Metodo que retorna el titulo de cada item'''
        return item.title
    
    def item_description(self, item):
        '''Metodo que retorna el contenido de cada item trucado a 30 palabras'''
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_update(self, item):
        '''Metodo que devuelve la fecha de publicación de cada post'''
        return item.publish