from django.contrib import admin
from .models import Project, BlogPost, Subscriber

admin.site.register(Project)
admin.site.register(BlogPost)
admin.site.register(Subscriber)
