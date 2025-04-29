from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
def is_staff_user(user):
    return user.is_staff or user.is_superuser

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')
        
        # First try to get the post regardless of status
        post = get_object_or_404(
            Post,
            publish_date__year=year,
            publish_date__month=month,
            publish_date__day=day,
            slug=slug
        )
        
        # Check if post is a draft and if user has permission to view it
        if post.status == 'draft':
            # Allow staff/superusers to view their own drafts
            if self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser):
                if self.request.user == post.author or self.request.user.is_superuser:
                    return post
            # If not staff or not the author, raise 404
            raise Http404("This post is not published yet")
        
        # If post is published, return it normally
        return post
    
    def get_context_data(self, **kwargs):
        # Rest of the method remains the same
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(approved=True)
        context['comment_form'] = CommentForm()
        context['categories'] = Category.objects.all()
        return context

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Post.objects.filter(
            categories=self.category,
            status='published'
        ).order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query),
                status='published'
            ).order_by('-publish_date')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        return context

# Admin views for staff and superusers
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class PostCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        return context

class PostUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context

class PostDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)

@login_required
@user_passes_test(is_staff_user)
def manage_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-publish_date')
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/manage_posts.html', {
        'posts': posts,
        'categories': Category.objects.all()
    })

@login_required
@user_passes_test(is_staff_user)
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.approved = True
    comment.save()
    messages.success(request, "Comment approved successfully!")
    return redirect('blog:post_detail', 
                   year=comment.post.publish_date.year,
                   month=comment.post.publish_date.month,
                   day=comment.post.publish_date.day,
                   slug=comment.post.slug)

@login_required
@user_passes_test(is_staff_user)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('blog:post_detail', 
                   year=post.publish_date.year,
                   month=post.publish_date.month,
                   day=post.publish_date.day,
                   slug=post.slug)

# Add these functions to your blog/views.py file

@login_required
@user_passes_test(is_staff_user)
def manage_categories(request):
    """View for managing categories"""
    categories = Category.objects.all().order_by('name')
    
    return render(request, 'blog/manage_categories.html', {
        'categories': categories
    })

@login_required
@user_passes_test(is_staff_user)
def category_create(request):
    """Create a new category without using forms"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        if name:
            # Check if category with this name already exists
            if Category.objects.filter(name__iexact=name).exists():
                messages.error(request, f"A category with name '{name}' already exists.")
                return redirect('blog:manage_categories')
            
            # Create new category
            category = Category(name=name, description=description)
            category.save()
            messages.success(request, f"Category '{name}' created successfully!")
        else:
            messages.error(request, "Category name cannot be empty.")
            
    return redirect('blog:manage_categories')

@login_required
@user_passes_test(is_staff_user)
def category_edit(request, category_id):
    """Display form to edit an existing category"""
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'blog/category_edit.html', {
        'category': category
    })

@login_required
@user_passes_test(is_staff_user)
def category_update(request, category_id):
    """Update an existing category"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        if name:
            # Check if another category with this name exists
            if Category.objects.filter(name__iexact=name).exclude(id=category_id).exists():
                messages.error(request, f"Another category with name '{name}' already exists.")
                return render(request, 'blog/category_edit.html', {'category': category})
            
            # Update category
            category.name = name
            category.description = description
            # If name changed, update slug
            if name.lower() != category.name.lower():
                category.slug = slugify(name)
            category.save()
            messages.success(request, f"Category '{name}' updated successfully!")
            return redirect('blog:manage_categories')
        else:
            messages.error(request, "Category name cannot be empty.")
            return render(request, 'blog/category_edit.html', {'category': category})
    
    return redirect('blog:manage_categories')

@login_required
@user_passes_test(is_staff_user)
def category_delete(request, category_id):
    """Delete an existing category"""
    category = get_object_or_404(Category, id=category_id)
    
    # Check if this category has posts
    if category.posts.count() > 0:
        messages.warning(request, f"Cannot delete category '{category.name}' because it has {category.posts.count()} posts.")
    else:
        category_name = category.name
        category.delete()
        messages.success(request, f"Category '{category_name}' deleted successfully!")
    
    return redirect('blog:manage_categories')