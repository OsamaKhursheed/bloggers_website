from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from shared_app.form import LoginForm
from shared_app.models import Like_blog,Blog
from blogger.models import blog_maker
from django.contrib import messages
from django.db.models import Count

from django.db.models import Count

def home_page(request):
    top_liked_blogs = Like_blog.objects.values('blog').annotate(like_count=Count('blog')).order_by('-like_count')[:9]
    top_blogs = Blog.objects.filter(id__in=[blog['blog'] for blog in top_liked_blogs])

    remaining_blogs = Blog.objects.exclude(id__in=top_blogs.values_list('id', flat=True)).order_by('-created_at')[:9]
    
    all_blogs = list(top_blogs) + list(remaining_blogs)
    
    return render(request, 'index.html', {'top_blogs': all_blogs})


def about_page(request):
    return render(request,'about_us.html')

def contact_page(request):
    return render(request,'contact_us.html')