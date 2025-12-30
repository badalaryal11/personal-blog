import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from blog.models import PageVisit
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
import datetime
import json

def debug_view():
    print("Starting debug...")
    try:
        # Aggregate PageViews by day
        chart_data = (
            PageVisit.objects.annotate(date=TruncDay('timestamp'))
            .values('date')
            .annotate(y=Count('id'))
            .order_by('date')
        )
        print("Chart data query created.")
        
        available_months = (
            PageVisit.objects.annotate(month=TruncMonth('timestamp'))
            .values('month')
            .annotate(c=Count('id'))
            .order_by('-month')
        )
        print("Available months query created.")

        now = timezone.now()
        selected_month = datetime.date(now.year, now.month, 1)
        print(f"Selected month: {selected_month}")

        if selected_month:
             chart_data = chart_data.filter(timestamp__year=selected_month.year, timestamp__month=selected_month.month)
        
        print("Filtering applied.")

        # Execute query
        data_list = list(chart_data)
        print(f"Chart data count: {len(data_list)}")
        
        as_json = json.dumps(data_list, default=str)
        print("JSON serialization successful.")
        
        available_months_list = list(available_months)
        print(f"Available months count: {len(available_months_list)}")

        months_choices = []
        for m in available_months_list:
            m_date = m['month']
            if m_date:
                value = m_date.strftime('%Y-%m')
                label = m_date.strftime('%B %Y')
                months_choices.append({'value': value, 'label': label})
        print("Months choices processed.")
        
    except Exception as e:
        print(f"ERROR CAUGHT: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_view()
