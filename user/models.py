from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import Permission, Group
# Create your models here.

# Модель користувача

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_admin = models.BooleanField(default=False)

    user_permissions = models.ManyToManyField(Permission, related_name='user_user_permissions')
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='user_groups',
        related_query_name='user',
    )

    def __str__(self):
        return self.username

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