from user.models import *
from network.models import *
from admin_tools.models import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import logging
# Create your views here.

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_admin

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        reason = request.POST.get('reason')
        user_to_delete = get_object_or_404(User, id=user_id)
        user_to_delete.delete()
        messages.success(request, f'User {user_to_delete.username} was deleted. Reason: {reason}')
        return redirect('user_management')

    return render(request, 'manage_users.html', {'users': users})

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