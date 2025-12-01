from django.shortcuts import render, get_object_or_404
from .models import Project, BlogPost

def home(request):
    projects = Project.objects.all().order_by('-created_at')
    posts = BlogPost.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'projects': projects, 'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
