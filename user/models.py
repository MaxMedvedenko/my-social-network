from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Модель користувача
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.username

# Модель друзів
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

# Модель підписок
class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)