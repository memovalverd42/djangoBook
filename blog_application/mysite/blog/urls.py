from django.urls import path
from .views import *
from .feeds import LastestPostsFeed

# Asignamos un nombre a la aplicación para poder acceder a sus propiedades
app_name = 'blog'
urlpatterns = [
    # Post views
    path('', post_list, name='post_list'),
    path(
        'tag/<slug:tag_slug>',
        post_list,
        name='post_list_by_tag',
    ),
    # path('', views.PostListView.as_view(), name='post_list'), # Para vistas basadas en clases
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',    # Forma de URL canonica
        post_detail,                                        # Vista controladora
        name='post_detail',                                 # Nombre del template
    ),
    path(
        '<int:post_id>/share/', 
        post_share, 
        name='post_share'
    ),
    path(
        '<int:post_id>/comment/', 
        post_comment, 
        name='post_comment'
    ),
    path(
        'feed/',
        LastestPostsFeed(),
        name='post_feed',
    ),
    path(
        'search/',
        post_search,
        name = 'post_search',
    ),
]