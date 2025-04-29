from django import forms
from .models import Post, Comment, Category
from django.utils.text import slugify

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'featured_image', 'categories', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control md-editor',
                'rows': 15,
                'placeholder': 'Write your content using Markdown'
            }),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
# Update the save method in PostForm in blog/forms.py
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:  # Only set slug if it doesn't exist
            instance.slug = slugify(instance.title)
        
        if commit:
            instance.save()
            self.save_m2m()  # This saves the categories
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Comment'})
        }