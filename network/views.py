from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.dateformat import DateFormat
from django.contrib import messages
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'index.html', context)



#--- Posts ---#

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


#--- Comments ---#

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
            formatted_date = DateFormat(comment.created_at).format('F j, Y, P')
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'user': comment.user.username,
                    'content': comment.content,
                    'created_at': formatted_date
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Content is required.'}, status=400)

    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        comment.content = new_content
        comment.save()
        return JsonResponse({'message': 'Comment updated successfully.'})

    return JsonResponse({'error': 'Invalid request.'}, status=400)

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



#--- Likes ---#

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            post.likes_count -= 1
        else:
            post.likes_count += 1

        post.save()

        return JsonResponse({'likes_count': post.likes_count})
    return JsonResponse({'error': 'Invalid request'}, status=400)

#--- Chats , messages ---#

@login_required
def chat_list_view(request):
    chats = request.user.chats.all()
    return render(request, 'chat_list.html', {'chats': chats})

@login_required
def create_chat_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        try:
            other_user = User.objects.get(username=username)
            chat = Chat.objects.create()
            chat.participants.add(request.user, other_user)
            return redirect('chat_list')
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, 'create_chat.html')

@login_required
def delete_chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user in chat.participants.all():
        chat.delete()
    return redirect('chat_list')

@login_required
def chat_detail_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all()
    
    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages})

@login_required
def send_message_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat=chat, sender=request.user, content=content)
            return redirect('chat_detail', chat_id=chat.id)

    return redirect('chat_detail', chat_id=chat.id)

@login_required
def edit_message_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        if message.sender == request.user:  # Check if the user is the sender
            content = request.POST.get('content')
            if content:
                message.content = content
                message.save()
                return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def delete_message_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        if message.sender == request.user:
            message.delete()
            return redirect('chat_detail', chat_id=message.chat.id)

    return render(request, 'delete_message.html', {'message': message})