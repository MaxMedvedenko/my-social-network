from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'index.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content:
            user = User.objects.get(pk=request.user.pk)
            post = Post(user=user, content=content, image=image)
            post.save()
            return redirect('index')
    return render(request, 'create_post.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Перевірка, чи поточний користувач є творцем поста
    if post.user != request.user:
        return render(request, 'post_detail.html', {'post': post})

    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Оновлення полів поста
        post.content = content
        if image:
            post.image = image
        post.save()

        return redirect('post_detail', post_id=post.id)

    return render(request, 'edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.user != request.user:
        return redirect('index')

    if request.method == 'POST':
        # Видалення поста
        post.delete()
        return redirect('index') 

    return render(request, 'delete_post.html', {'post': post})