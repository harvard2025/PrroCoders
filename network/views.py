from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json

from .models import User, Post, Comment, Notification, Trend, Message


def index(request):
    """Show the community homepage with all posts"""
    # Get all posts
    posts = Post.objects.all().order_by('-created_at')
    
    # Paginate posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get trending topics
    trends = Trend.objects.all()[:5]
    
    # Render the index template with the data
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "trends": trends
    })


@login_required
def create_post(request):
    """Create a new post"""
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")
        
        # Create post
        post = Post(user=request.user, content=content, image=image)
        post.save()
        
        # Extract hashtags
        words = content.split()
        hashtags = [word[1:] for word in words if word.startswith("#")]
        
        # Update trends
        for tag in hashtags:
            trend, created = Trend.objects.get_or_create(name=tag)
            trend.post_count += 1
            trend.save()
        
        # Redirect to homepage
        return HttpResponseRedirect(reverse("network:index"))
    
    # If GET request, redirect to homepage
    return HttpResponseRedirect(reverse("network:index"))


def profile(request, username):
    """Show user profile"""
    # Get user
    profile_user = get_object_or_404(User, username=username)
    
    # Get user posts
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    
    # Paginate posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check if current user follows profile user
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.following.filter(id=profile_user.id).exists()
    
    # Render profile template with data
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "is_following": is_following,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count()
    })


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == "POST":
        # Get form data
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.bio = request.POST.get("bio")
        user.location = request.POST.get("location")
        user.website = request.POST.get("website")
        
        # Check if profile image was uploaded
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES.get("profile_image")
        
        # Save changes
        user.save()
        
        # Redirect to profile page
        return redirect("network:profile", username=user.username)
    
    # If GET request, show edit profile form
    return render(request, "network/edit_profile.html")


@csrf_exempt
@login_required
def follow(request, user_id):
    """Follow or unfollow user"""
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get user to follow/unfollow
    try:
        user_to_follow = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    # Check if already following
    is_following = request.user.following.filter(id=user_to_follow.id).exists()
    
    if is_following:
        # Unfollow
        request.user.following.remove(user_to_follow)
        return JsonResponse({"status": "unfollowed", "followers_count": user_to_follow.followers.count()})
    else:
        # Follow
        request.user.following.add(user_to_follow)
        
        # Create notification
        notification = Notification(
            recipient=user_to_follow,
            sender=request.user,
            notification_type='follow'
        )
        notification.save()
        
        return JsonResponse({"status": "followed", "followers_count": user_to_follow.followers.count()})


@csrf_exempt
@login_required
def like_post(request, post_id):
    """Like or unlike a post"""
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Check if already liked
    is_liked = request.user in post.likes.all()
    
    if is_liked:
        # Unlike
        post.likes.remove(request.user)
        return JsonResponse({"status": "unliked", "likes_count": post.likes.count()})
    else:
        # Like
        post.likes.add(request.user)
        
        # Create notification (only if the user is not liking their own post)
        if request.user != post.user:
            notification = Notification(
                recipient=post.user,
                sender=request.user,
                notification_type='like',
                post=post
            )
            notification.save()
        
        return JsonResponse({"status": "liked", "likes_count": post.likes.count()})


@csrf_exempt
@login_required
def comment_post(request, post_id):
    """Add a comment to a post"""
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Get comment content
    data = json.loads(request.body)
    content = data.get("content")
    
    if not content:
        return JsonResponse({"error": "Comment content is required."}, status=400)
    
    # Create comment
    comment = Comment(user=request.user, post=post, content=content)
    comment.save()
    
    # Create notification (only if the user is not commenting on their own post)
    if request.user != post.user:
        notification = Notification(
            recipient=post.user,
            sender=request.user,
            notification_type='comment',
            post=post,
            comment=comment
        )
        notification.save()
    
    # Return comment data
    return JsonResponse(comment.serialize(), status=201)


@csrf_exempt
@login_required
def edit_post(request, post_id):
    """Edit a post"""
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    # Get post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Check if the user is the author of the post
    if post.user != request.user:
        return JsonResponse({"error": "You can only edit your own posts."}, status=403)
    
    # Get new content
    data = json.loads(request.body)
    content = data.get("content")
    
    if not content:
        return JsonResponse({"error": "Content is required."}, status=400)
    
    # Update post
    post.content = content
    post.save()
    
    # Return updated post
    return JsonResponse(post.serialize())


@login_required
def delete_post(request, post_id):
    """Delete a post"""
    # Get post
    post = get_object_or_404(Post, pk=post_id)
    
    # Check if the user is the author of the post
    if post.user != request.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect("network:index")
    
    # Delete post
    post.delete()
    
    # Redirect to previous page
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect("network:index")


def search(request):
    """Search for users, posts, and trends"""
    query = request.GET.get('q', '')
    
    if query:
        # Search users
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
        
        # Search posts
        posts = Post.objects.filter(content__icontains=query).order_by('-created_at')
        
        # Search trends
        trends = Trend.objects.filter(name__icontains=query)
        
        # Paginate posts
        paginator = Paginator(posts, 10)  # Show 10 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Render search results
        return render(request, "network/search.html", {
            "query": query,
            "users": users,
            "page_obj": page_obj,
            "trends": trends
        })
    
    # If no query, redirect to homepage
    return redirect("network:index")


def trending(request):
    """Show trending topics"""
    trends = Trend.objects.all()
    
    # Render trending page
    return render(request, "network/trending.html", {
        "trends": trends
    })


def trend_posts(request, trend_name):
    """Show posts for a specific trend"""
    trend = get_object_or_404(Trend, name=trend_name)
    
    # Get posts with the trend
    posts = Post.objects.filter(content__icontains=f"#{trend_name}").order_by('-created_at')
    
    # Paginate posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Render trend posts page
    return render(request, "network/trend_posts.html", {
        "trend": trend,
        "page_obj": page_obj
    })


@login_required
def notifications(request):
    """Show user notifications"""
    # Mark all notifications as read
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    
    # Get all notifications
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Render notifications page
    return render(request, "network/notifications.html", {
        "notifications": notifications
    })


@login_required
def unread_notifications_count(request):
    """Get unread notifications count"""
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({"count": count})


@login_required
def messages_view(request):
    """Show user messages"""
    # Get all conversations
    conversations = User.objects.filter(
        Q(sent_messages__recipient=request.user) | Q(received_messages__sender=request.user)
    ).distinct()
    
    # Render messages page
    return render(request, "network/messages.html", {
        "conversations": conversations
    })


@login_required
def conversation(request, username):
    """Show conversation with a specific user"""
    # Get other user
    other_user = get_object_or_404(User, username=username)
    
    if request.method == "POST":
        # Send message
        content = request.POST.get("content")
        
        message = Message(sender=request.user, recipient=other_user, content=content)
        message.save()
        
        # Redirect to conversation
        return redirect("network:conversation", username=username)
    
    # Get messages
    messages_list = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) | 
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('created_at')
    
    # Mark messages as read
    messages_list.filter(sender=other_user, recipient=request.user, is_read=False).update(is_read=True)
    
    # Render conversation page
    return render(request, "network/conversation.html", {
        "other_user": other_user,
        "messages": messages_list
    })


@login_required
def unread_messages_count(request):
    """Get unread messages count"""
    count = Message.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({"count": count})