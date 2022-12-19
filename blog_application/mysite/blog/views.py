from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    post_list = Post.published.all()

    # Paginacion con 3 posts por pagina
    paginator = Paginator(post_list, 3)      # Creamos objeto de paginacion
    page_number = request.GET.get('page', 1)
    try: 
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Si page_number es diferente de un int
        posts = paginator.page(1)
    except EmptyPage:
        # Si page_number está fuera de rango
        posts = paginator.page(paginator.num_pages)

    return render(request,
                'blog/post/list.html',
                {'posts': posts}
            )

def post_detail(request, year, month, day, post):
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
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISHED,
        slug = post,
        publish__year = year,
        publish__month = month,
        publish__day = day
    )

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )



