from django.db import models 
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Manager para gestionar posts por estado de publicación
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.PUBLISHED
        )

# Modelo (Tabla) Post para la base de datos
class Post(models.Model):
    """Modelo para post en la base de datos"""
    # Subclase para crear opciones para los campos de la DB
    class Status(models.TextChoices):
        DRAFT     = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title   = models.CharField(max_length=250)
    slug    = models.SlugField(
                        max_length=250,
                        # unique_for_date -> Indica que cada campo 'slug' debe de
                        # ser unico por cada fecha de campo 'publish' 
                        # para que las URL sean unicas
                        unique_for_date='publish', 
                    )
    # Llave foranea que apunta a Modelo User 
    author  = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                # related_name -> este atributo permite darle un nombre
                                # a la relación entre los dos objetos
                                related_name='blog_posts')

    body    = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status  = models.CharField(max_length=2,
                              # choises -> Este parametro permite asociar opciones
                              # establecidas en la subclase 'Status', permitiendo
                              # establecer solo las opciones que están en el modelo
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    # Manager's
    objects   = models.Manager()   # El manager por default
    published = PublishedManager() # El manager custom para publicaciones
    tags      = TaggableManager()  # Manager para tags

    class Meta:
        ordering = ['-publish']                # Ordenar descendente
        # Agregar un index a la base de datos para mejorar la busqueda
        # dentro de la DB por publicación
        indexes  = [
            models.Index(fields=['-publish']),
        ]

    # Crear URL canonicas
    def get_absolute_url(self):  
        return reverse(
            # URL apuntando a la vista blog_detail
            'blog:post_detail',          
            # Atributos que formarán parte de la URL
            args = [
                    self.publish.year,
                    self.publish.month,
                    self.publish.day,
                    self.slug
                ]
        )

    def __str__(self):
        return self.title  

# Modelo (tabla) Comment para guardar los comentarios de los usuarios
class Comment(models.Model):
    # LLave foranea para apuntar y relacionar a Modelo Post
    post    = models.ForeignKey(
                        Post,
                        on_delete=models.CASCADE,
                        # related_name -> este atributo permite darle un nombre
                        # a la relación entre los dos objetos
                        related_name='comments'
                    )
    name    = models.CharField(max_length=255)
    email   = models.EmailField()
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)

    class Meta:
        # Orden de manera cronologica
        ordering = ['created']     
        # Index para la base de datos
        indexes = [                
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'