from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Project, BlogPost

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            try:
                send_mail(
                    subject=f'Portfolio Contact: {name}',
                    message=f'From: {name} <{email}>\n\n{message}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['badal.aryal@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, 'An error occurred while sending your message. Please try again later.')
        else:
            messages.error(request, 'Please fill in all fields.')
            
        return redirect('home')

    projects = Project.objects.all().order_by('-created_at')
    posts = BlogPost.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'projects': projects, 'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
