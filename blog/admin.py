from django.contrib import admin
from .models import Project, BlogPost, Subscriber, PageVisit, Donation

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
        from django.db.models.functions import TruncDay, TruncMonth
        from django.utils import timezone
        import datetime
        import json

        # Aggregate PageViews by day
        try:
            chart_data_qs = (
                PageVisit.objects.annotate(date=TruncDay('timestamp'))
                .values('date')
                .annotate(y=Count('id'))
                .order_by('date')
            )

            # Get all available months for the dropdown
            available_months_qs = (
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

            if selected_month and chart_data_qs.exists():
                chart_data_qs = chart_data_qs.filter(timestamp__year=selected_month.year, timestamp__month=selected_month.month)

            chart_data = list(chart_data_qs)
            as_json = json.dumps(chart_data, default=str)
            
            # Prepare available months list for template
            months_choices = []
            for m in available_months_qs:
                m_date = m['month']
                if m_date:
                    value = m_date.strftime('%Y-%m')
                    label = m_date.strftime('%B %Y')
                    months_choices.append({'value': value, 'label': label})

        except Exception as e:
            print(f"Error in PageVisitAdmin: {e}")
            as_json = '[]'
            months_choices = []
            selected_month = None

        extra_context = extra_context or {}
        extra_context['chart_data'] = as_json
        extra_context['months_choices'] = months_choices
        extra_context['selected_month'] = selected_month.strftime('%Y-%m') if selected_month else ''

        return super().changelist_view(request, extra_context=extra_context)

    list_display = ('path', 'timestamp', 'ip_address')
    list_filter = ('timestamp',)
    search_fields = ('path', 'ip_address')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'status', 'created_at', 'esewa_ref_id')
    list_filter = ('timestamp', 'status') if hasattr(Donation, 'timestamp') else ('created_at', 'status')
    search_fields = ('name', 'transaction_id', 'esewa_ref_id')
