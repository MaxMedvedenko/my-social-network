from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login, login, logout, authenticate

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from user.models import *
from network.models import Post

from django.shortcuts import get_object_or_404

from django.http import JsonResponse
# Create your views here.

# Register --- Login --- Logout #

def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Неправильне ім'я користувача або пароль. Будь ласка, спробуйте ще раз."

    return render(request, 'login.html', {'error_message': error_message})

def register_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if password1 != password2:
            error_message = "Паролі не співпадають."
        else:
            try:
                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.set_password(password1)
                user.full_clean()
                user.save()
                login(request, user)
                return redirect('index')
            except ValidationError as e:
                error_message = e.messages[0]
            except IntegrityError:
                error_message = "Ім'я користувача вже існує. Будь ласка, виберіть інше ім'я користувача."

    return render(request, 'register.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('index'))

# --- Profile --- #

@login_required
def profile_view(request, username):
    # Отримати профіль користувача
    profile = get_object_or_404(Profile, user__username=username)

    # Перевірити, чи є користувач другом
    is_friend = Friend.objects.filter(user=request.user, friend=profile.user).exists() or \
                Friend.objects.filter(user=profile.user, friend=request.user).exists()

    # Ініціалізувати змінні для запитів
    has_sent_request = False
    has_received_request = False
    request_id = None

    # Перевірити, чи відправлено запит
    friendship_sent = Friendship.objects.filter(from_user=request.user, to_user=profile.user, status='pending').first()
    if friendship_sent:
        has_sent_request = True
        request_id = friendship_sent.id

    # Перевірити, чи отримано запит
    friendship_received = Friendship.objects.filter(from_user=profile.user, to_user=request.user, status='pending').first()
    if friendship_received:
        has_received_request = True
        request_id = friendship_received.id

    # Отримати пости користувача
    posts = Post.objects.filter(user=profile.user).order_by('-created_at')

    # Передати всі дані в контекст шаблону
    context = {
        'profile': profile,
        'is_friend': is_friend,
        'has_sent_request': has_sent_request,
        'has_received_request': has_received_request,
        'request_id': request_id,
        'posts': posts,
    }
    
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        profile.bio = request.POST['bio']
        profile.phone_number = request.POST['phone_number']

        avatar = request.FILES.get('avatar')
        if avatar:
            profile.avatar = avatar

        birth_date = request.POST.get('birth_date')
        if birth_date:
            profile.birth_date = birth_date

        user.save()
        profile.save()
        return redirect('profile_view', username=user.username)

    return render(request, 'edit_profile.html', {'user': user, 'profile': profile})


# --- Friend --- #

@login_required
def friends_list_view(request):
    # Отримати всі пари друзів, в яких користувач є або `user`, або `friend`
    friends = Friend.objects.filter(user=request.user) | Friend.objects.filter(friend=request.user)

    # Витягти унікальних друзів
    unique_friends = set()
    for friendship in friends:
        if friendship.user == request.user:
            unique_friends.add(friendship.friend)
        else:
            unique_friends.add(friendship.user)

    return render(request, 'friends_list.html', {'friends': unique_friends})

@login_required
def friend_requests_view(request):
    incoming_requests = Friendship.objects.filter(to_user=request.user, status='pending')
    outgoing_requests = Friendship.objects.filter(from_user=request.user, status='pending')
    
    return render(request, 'friend_requests.html', {
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests
    })

@login_required
def send_friend_request(request, user_id):
    target_user = get_object_or_404(Profile, user_id=user_id)
    if target_user.user == request.user:
        return redirect('profile_view', username=target_user.user.username)
    
    existing_request = Friendship.objects.filter(from_user=request.user, to_user=target_user.user).exists()
    if existing_request:
        return redirect('profile_view', username=target_user.user.username)

    Friendship.objects.create(from_user=request.user, to_user=target_user.user, status='pending')
    return redirect('profile_view', username=target_user.user.username)

@login_required
def cancel_friend_request(request, request_id):
    # Дістаємо запит дружби, який потрібно скасувати
    friend_request = get_object_or_404(Friendship, id=request_id, from_user=request.user)

    if friend_request:
        # Видалити запит дружби
        friend_request.delete()

    return redirect('friend_requests')

@login_required
def accept_friend_request(request, request_id):
    # Отримати об'єкт запиту на дружбу
    friend_request = get_object_or_404(Friendship, id=request_id, to_user=request.user, status='pending')
    
    # Перевірити, чи запит існує і має статус 'pending'
    if friend_request:
        # Змінити статус запиту на 'accepted'
        friend_request.status = 'accepted'
        friend_request.save()

        # Створити записи в моделі Friend для обох користувачів
        Friend.objects.get_or_create(user=friend_request.from_user, friend=friend_request.to_user)
        Friend.objects.get_or_create(user=friend_request.to_user, friend=friend_request.from_user)

        # Видалити запис запиту на дружбу
        friend_request.delete()

    # Перенаправити користувача до списку запитів на дружбу
    return redirect('friend_requests')


@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(Friendship, id=request_id, to_user=request.user)
    if friend_request:
        friend_request.delete()
    return redirect('friend_requests')

@login_required
def unfriend(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    
    Friend.objects.filter(user=request.user, friend=profile.user).delete()
    Friend.objects.filter(user=profile.user, friend=request.user).delete()
    
    return redirect('profile_view', username=profile.user.username)