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

from .forms import SubscriptionForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            
            # Send confirmation email
            try:
                send_mail(
                    subject='Welcome to my Newsletter!',
                    message='Thank you for subscribing to my newsletter. I will keep you updated with my latest blog posts and projects.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscriber.email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log error but don't fail the response
                print(f"Error sending email: {e}")

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
            else:
                messages.success(request, 'Thank you for subscribing!', extra_tags='subscription')
                return redirect('/#newsletter')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Invalid email or already subscribed.'})
            else:
                messages.error(request, 'Invalid email or already subscribed.', extra_tags='subscription')
                return redirect('/#newsletter')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    else:
        return redirect('/')
