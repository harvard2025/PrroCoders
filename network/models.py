from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """User model extending Django's AbstractUser"""
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    
    # Add related_name to avoid clash with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='network_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='network_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.username
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "profile_image": self.profile_image.url if self.profile_image else None,
            "followers_count": self.followers.count(),
            "following_count": self.following.count()
        }


class Post(models.Model):
    """Post model for user posts (tweets)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}..."
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "content": self.content,
            "image": self.image.url if self.image else None,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "likes_count": self.likes.count(),
            "comments_count": self.comments.count(),
            "is_edited": self.created_at != self.edited_at
        }


class Comment(models.Model):
    """Comment model for post comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} comment on {self.post}"
    
    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post.id,
            "user": self.user.serialize(),
            "content": self.content,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "likes_count": self.likes.count()
        }


class Notification(models.Model):
    """Notification model for user notifications"""
    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('mention', 'Mention')
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient.username}"


class Message(models.Model):
    """Direct message model for private messaging"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


class Trend(models.Model):
    """Trending topics model"""
    name = models.CharField(max_length=100, unique=True)
    post_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-post_count']
    
    def __str__(self):
        return self.name