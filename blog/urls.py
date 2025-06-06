from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    # Public-facing URLs
     path('category/create/', views.category_create, name='category_create'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', 
         views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', 
         views.CategoryPostListView.as_view(), name='category'),
    path('search/', 
         views.SearchResultsView.as_view(), name='search_results'),
    
    # Admin URLs (staff only)
    path('manage/', views.manage_posts, name='manage_posts'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('comment/<int:comment_id>/approve/', views.approve_comment, name='approve_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # Category management URLs
    path('manage/categories/', views.manage_categories, name='manage_categories'),

    path('category/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:category_id>/update/', views.category_update, name='category_update'),
    path('category/<int:category_id>/delete/', views.category_delete, name='category_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)