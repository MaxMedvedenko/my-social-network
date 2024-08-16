from user.models import *
from network.models import *
from admin_tools.models import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
import logging
from django.db.models import Q
# Create your views here.

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_admin

login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

login_required
@user_passes_test(is_admin)
def manage_users(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(
            username__icontains=search_query
        ) | User.objects.filter(
            email__icontains=search_query
        ) | User.objects.filter(
            first_name__icontains=search_query
        ) | User.objects.filter(
            last_name__icontains=search_query
        )
    else:
        users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        reason = request.POST.get('reason')
        user_to_delete = get_object_or_404(User, id=user_id)
        logger.info(f'User {user_to_delete.username} deleted. Reason: {reason}')
        user_to_delete.delete()
        messages.success(request, f'User {user_to_delete.username} was deleted. Reason: {reason}')
        return redirect('user_management')

    return render(request, 'manage_users.html', {'users': users})

login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        logger.info(f'User {user_to_delete.username} deleted. Reason: {reason}')
        user_to_delete.delete()
        messages.success(request, f'User {user_to_delete.username} was deleted. Reason: {reason}')
        return redirect('user_management')
    return redirect('user_management')

# @login_required
# @user_passes_test(is_admin)
# def manage_posts(request):
#     posts = Post.objects.all().order_by('-created_at')

#     context = {
#         'posts': posts,
#     }

#     return render(request, 'manage_posts.html', context)

@login_required
@user_passes_test(is_admin)
def manage_posts(request):
    query = request.GET.get('post_search', '')
    posts = Post.objects.all().order_by('-created_at')
    
    if query:
        posts = posts.filter(
            content__icontains=query
        ) | posts.filter(
            user__username__icontains=query
        )

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        reason = request.POST.get('reason')
        post_to_delete = get_object_or_404(Post, id=post_id)
        logger.info(f'Post by {post_to_delete.user.username} deleted. Reason: {reason}')
        post_to_delete.delete()
        messages.success(request, f'Post by {post_to_delete.user.username} was deleted. Reason: {reason}')
        return redirect('manage_posts')

    return render(request, 'manage_posts.html', {
        'posts': posts,
        'query': query,
    })


@login_required
@user_passes_test(is_admin)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post has been successfully deleted.')
        return redirect('manage_posts')

    return render(request, 'delete_post_confirmation.html', {'post': post})