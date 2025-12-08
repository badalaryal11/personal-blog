from django.contrib import admin
from .models import Project, BlogPost, Subscriber, PageVisit

admin.site.register(Project)
admin.site.register(BlogPost)
admin.site.register(Subscriber)

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'timestamp', 'ip_address')
    list_filter = ('timestamp',)
    search_fields = ('path', 'ip_address')
