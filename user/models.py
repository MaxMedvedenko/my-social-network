from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import ValidationError

from .models import *
# Create your models here.

# Модель користувача

class User(AbstractUser):

    def __str__(self):
        return self.username

    # Password validation
    def clean(self):
        super().clean()
        if len(self.password) < 8:
            raise ValidationError("Your password must contain at least 8 characters.")
        if self.password.isdigit():
            raise ValidationError("Your password can’t be entirely numeric.")
        if self.password.isalpha():
            raise ValidationError("Your password must contain at least one digit.")
        if self.password.islower() or self.password.isupper():
            raise ValidationError("Your password must contain both uppercase and lowercase letters.")
        if not any(char.isdigit() for char in self.password):
            raise ValidationError("Your password must contain at least one digit.")
        if not any(char.isupper() for char in self.password) or not any(char.islower() for char in self.password):
            raise ValidationError("Your password must contain both uppercase and lowercase letters.")
        if not any(char.isalnum() for char in self.password):
            raise ValidationError("Your password must contain at least one special character.")
        if self.password.lower() in ['password', '123456', 'qwerty']:
            raise ValidationError("Your password is too common.")

# Модель профілю

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Створити сигнал для автоматичного створення профілю при створенні нового користувача
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Модель друзів

# class Friend(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
#     friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_users')

#     def __str__(self):
#         return f"{self.user.username} <-> {self.friend.username}"

#     class Meta:
#         unique_together = ['user', 'friend']

# Модель запитів у друзів

# class FriendRequest(models.Model):
#     from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)

# Модель підписок

# class Follow(models.Model):
#     user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
#     following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)