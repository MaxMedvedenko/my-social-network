from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login, login, logout, authenticate

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from user.models import User

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
            return redirect('index')  # URL головної сторінки
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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                login(request, user)  # Вхід користувача в систему після реєстрації
                return redirect('index')  # URL головної сторінки
            except IntegrityError:
                error_message = "Ім'я користувача вже існує. Будь ласка, виберіть інше ім'я користувача."
        else:
            error_message = "Паролі не співпадають."
    
    return render(request, 'register.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('index'))

# --- Profile --- #

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        bio = request.POST['bio']
        avatar = request.FILES.get('avatar')
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.bio = bio
        if avatar:
            user.avatar = avatar
        user.save()
        return redirect('profile')
    
    context = {'user': user}
    return render(request, 'edit_profile.html', context)
