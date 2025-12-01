import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from blog.models import Project, BlogPost

# Projects
p1 = Project(
    title='Weather App',
    description='A beautiful weather application built with Swift and OpenWeatherMap API.',
    image_url='https://images.unsplash.com/photo-1592210454359-9043f067919b?auto=format&fit=crop&w=1000&q=80',
    link='https://github.com/badalaryal/weather-app',
    tech_stack='Swift, UIKit, API'
)
p1.save()

p2 = Project(
    title='Task Manager',
    description='A productivity tool to manage daily tasks efficiently.',
    image_url='https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=1000&q=80',
    link='https://github.com/badalaryal/task-manager',
    tech_stack='Python, Django, React'
)
p2.save()

# Blog Posts
b1 = BlogPost(
    title='Getting Started with iOS Development',
    content='iOS development is an exciting journey. In this post, we will explore the basics of Swift and Xcode...'
)
b1.save()

b2 = BlogPost(
    title='Why I Love Python',
    content='Python is a versatile language that can be used for web development, data science, and more. Here is why it is my favorite...'
)
b2.save()

print('Data populated.')
