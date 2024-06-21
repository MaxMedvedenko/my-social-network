from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
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