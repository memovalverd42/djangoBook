from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.db.models import Count
# from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, \
                                            TrigramSimilarity

# class PostListView(ListView):
#     """
#     Es una alternativa a la funcion post_list(request)
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

# Vista post_list
def post_list(request, tag_slug=None):
    """
    Vista que lista todos los posts en template -> list.html
    """
    # Obtener todos los posts a traves del Manager custom -> published
    post_list = Post.published.all()   
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Paginacion con 3 posts por pagina
    paginator   = Paginator(post_list, 3)            # Creamos objeto de paginacion
    page_number = request.GET.get('page', 1)         # Obetenemos la primera pagina
    # Try para acceder a numero de pagina solicitado a traves del request
    try: 
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Si page_number es diferente de un int
        posts = paginator.page(1)
    except EmptyPage:
        # Si page_number está fuera de rango
        posts = paginator.page(paginator.num_pages)

    # Finalmente, retornamos los posts hacia el template list.html
    return render(request,
                'blog/post/list.html',
                {'posts': posts, 'tag': tag}
            )

# Vista post_detail
def post_detail(request, year, month, day, post):
    """
    Vista que muestra un post completo en template -> detail.html
    """
    # PRIMERA FORMA
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No se encontró el Post :(")
    
    # return render(
    #     request,
    #     'blog/post/detail.html',
    #     {'post': post}
    # )

    # SEGUNDA FORMA
    # Para mostrar los detalles de un post y además con una URL canonica
    # usamos tres parametros, se ingresan en la función que buscará el elemento
    # que coincida con los parametros o si no retorna un error 404 (no encontrado)
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISHED,
        slug = post,
        publish__year = year,
        publish__month = month,
        publish__day = day
    )

    # Obteniendo todos los comentarios activos
    # Usando el atributo related_name = 'comments' desde el modelo Comment()
    comments = post.comments.filter(active=True) 

    # Formulario para comentarios de usuarios
    form = CommentForm()

    # Listado de posts similares
    # Recuperamos una lista de los tags asociados al post
    post_tags_ids = post.tags.values_list('id', flat=True)                  
    # Recuperamos los posts que contengan los tags anteriormente recuperados (excluyendo el actual)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                    .exclude(id=post.id)
    
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags', '-publish')[:4]



    # Finalmente, retornamos el post a visualizar, los comentarios de ese
    # post y el formulario para plasmarlo en el template detail.html
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )

# Vista post_share
def post_share(request, post_id):
    """
    Vista que genera formulario para compartir un post via email -> share.html
    """
    # Recuperar el post por ID
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    # Variable para verificar si se ha enviado correctamente el mail
    sent = False
    # Si llega una petición de tipo POST...
    if request.method == 'POST':
        # Enviar formulario
        form = EmailPostForm(request.POST)
        # Si los campos pasan la validación
        if form.is_valid():
            # Obtenemos diccionario con datos del formulario
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} te recomienda leer {post.title}"
            message = f"Dale una leida a {post.title} en {post_url}\n\n" \
                      f"{data['name']}\'s comments: {data['comments']}"
            send_mail(
                    subject, 
                    message, 
                    'guillermovalverde42@gmail.com',
                    [data['to']]
                )
            # Una vez enviado el mail, confirmamos con la variable sent
            sent = True 
    # Si no hay petición de tipo post, entonces no hay datos que procesar
    else:
        form = EmailPostForm()
    
    # Finalmente se retorna el post compartido, el formulario para dibujar en el template
    # y la variable sent para poder saber si se ha enviado o no el mail
    return render(
        request, 
        'blog/post/share.html', 
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )

# Vista post_comment
@require_POST
def post_comment(request, post_id):
    """
    Vista que genera formulario para crear comentario en un post -> comment.html
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    # Variable vacia para guardar el comentario
    comment = None
    # Creamos instancia de CommentForm con los datos POST del request
    form = CommentForm(data=request.POST)
    # Si la validación de datos es correcta
    if form.is_valid():
        # Crear un comentario sin guardarlo
        comment = form.save(commit=False)
        # Asignamos el post al comentario
        comment.post = post
        # Ahora si, guardamos el comentario en la DB
        comment.save()
    
    # Finalmente, retornamos el post, el comentario y el formulario para dibujar 
    # en la plantilla comment.html
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', config='spanish', weight='A') + \
                            SearchVector('body', config='spanish', weight='B')
            search_query = SearchQuery(query, config='spanish')
            results = Post.published.annotate(
                search = search_vector,
                rank = SearchRank(search_vector, search_query),
            ).filter(rank__gte=0.3).order_by('-rank')

    # if 'query' in request.GET:
    #     form = SearchForm(request.GET)
    #     if form.is_valid():
    #         query = form.cleaned_data['query']
    #         results = Post.published.annotate(
    #             similarity=TrigramSimilarity('title', query),
    #         ).filter(similarity__gt=0.1).order_by('-similarity')
    
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )