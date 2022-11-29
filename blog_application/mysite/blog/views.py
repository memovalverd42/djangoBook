from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
from .models import Post

def post_list(request):
    posts = Post.published.all()
    return render(request,
                'blog/post/list.html',
                {'posts': posts}
            )

def post_detail(request, id):
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
        id=id,
        status=Post.Status.PUBLISHED,
    )

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )



