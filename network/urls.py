from django.urls import path
from . import views

app_name = "network"

urlpatterns = [
    # Main views
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("search", views.search, name="search"),
    path("trending", views.trending, name="trending"),
    path("trend/<str:trend_name>", views.trend_posts, name="trend_posts"),
    path("notifications", views.notifications, name="notifications"),
    path("messages", views.messages_view, name="messages"),
    path("messages/<str:username>", views.conversation, name="conversation"),
    
    # Action views
    path("post", views.create_post, name="create_post"),
    path("post/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/like", views.like_post, name="like_post"),
    path("post/<int:post_id>/comment", views.comment_post, name="comment_post"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    
    # API endpoints
    path("api/notifications/count", views.unread_notifications_count, name="unread_notifications_count"),
    path("api/messages/count", views.unread_messages_count, name="unread_messages_count"),
]