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

    # Отримання коментарів поточного користувача
    current_user_comments = Comment.objects.filter(post=post, user=request.user).order_by('-created_at')

    # Отримання всіх інших коментарів, відсортованих від новіших до старіших
    other_comments = Comment.objects.filter(post=post).exclude(user=request.user).order_by('-created_at')

    # Об'єднання коментарів для відображення в шаблоні
    comments = list(current_user_comments) + list(other_comments)

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.user != request.user:
        return render(request, 'post_detail.html', {'post': post})

    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')

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
        post.delete()
        return redirect('index') 

    return render(request, 'delete_post.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                created_at=timezone.now()
            )
            return redirect('post_detail', post_id=post_id)
        else:
            pass
    
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)

# doesn't work
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        pass
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
            return redirect('post_detail', post_id=comment.post.id)
        else:
            pass
    
    context = {
        'comment': comment,
        'edit_mode': True,
    }
    return render(request, 'post_detail.html', context)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        pass

    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        return redirect('post_detail', post_id=post_id)
    
    context = {
        'comment': comment,
    }
    return render(request, 'delete_comment.html', context)