from django.contrib import admin
from .models import Project, BlogPost, Subscriber, PageVisit

admin.site.site_header = "Portfolio Administration"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to the Portfolio Admin"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'tech_stack', 'created_at')
    search_fields = ('title', 'description', 'tech_stack')
    list_filter = ('created_at',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'canonical_url')
    search_fields = ('title', 'content')
    list_filter = ('date_posted',)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    change_list_template = 'admin/blog/pagevisit/change_list.html'

    def changelist_view(self, request, extra_context=None):
        from django.db.models import Count
        from django.db.models.functions import TruncDay
        import json
        import datetime
        from django.utils import timezone

        # Aggregate PageViews by day
        chart_data = (
            PageVisit.objects.annotate(date=TruncDay('timestamp'))
            .values('date')
            .annotate(y=Count('id'))
            .order_by('date')
        )

        # Get all available months for the dropdown
        # This is a bit expensive if lots of data, sticking to simple approach for now or optimizing with TruncMonth
        from django.db.models.functions import TruncMonth
        available_months = (
            PageVisit.objects.annotate(month=TruncMonth('timestamp'))
            .values('month')
            .annotate(c=Count('id'))
            .order_by('-month')
        )

        # Filter logic
        selected_month_str = request.GET.get('month')
        
        if selected_month_str:
             try:
                selected_month = datetime.datetime.strptime(selected_month_str, '%Y-%m').date()
             except ValueError:
                selected_month = None
        else:
             # Default to current month if valid or latest available
            now = timezone.now()
            selected_month = datetime.date(now.year, now.month, 1)


        if selected_month:
             chart_data = chart_data.filter(timestamp__year=selected_month.year, timestamp__month=selected_month.month)

        as_json = json.dumps(list(chart_data), default=str)
        
        extra_context = extra_context or {}
        extra_context['chart_data'] = as_json
        
        # Prepare available months list for template
        # Format: "2023-10" (value), "October 2023" (display)
        months_choices = []
        for m in available_months:
            m_date = m['month']
            if m_date:
                value = m_date.strftime('%Y-%m')
                label = m_date.strftime('%B %Y')
                months_choices.append({'value': value, 'label': label})

        extra_context['months_choices'] = months_choices
        extra_context['selected_month'] = selected_month.strftime('%Y-%m') if selected_month else ''

        return super().changelist_view(request, extra_context=extra_context)

    list_display = ('path', 'timestamp', 'ip_address')
    list_filter = ('timestamp',)
    search_fields = ('path', 'ip_address')
