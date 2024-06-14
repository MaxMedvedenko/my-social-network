from django.db import models

from django.utils import timezone
from user.models import User

# Create your models here.

# Модель публікації
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[:20]

# Модель лайків
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

# Модель коментарів
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

# Модель групи
class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(User, through='GroupMember')

# Модель учасника групи
class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)

# Модель публікації в групі
class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

# Модель приватних повідомлень
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

# Модель сповіщень
# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.CharField(max_length=255)
#     created_at = models.DateTimeField(default=timezone.now)
#     is_read = models.BooleanField(default=False)

# Модель відгуків
# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     content = models.TextField()
#     rating = models.IntegerField(default=0)
#     created_at = models.DateTimeField(default=timezone.now)

# Модель для налаштувань сповіщень
# class NotificationSetting(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     notify_messages = models.BooleanField(default=True)
#     notify_friend_requests = models.BooleanField(default=True)
#     notify_comments = models.BooleanField(default=True)
#     notify_likes = models.BooleanField(default=True)
#     notify_group_posts = models.BooleanField(default=True)