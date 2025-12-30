import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from blog.models import PageVisit

# Clear existing visits? Optional, maybe keep them.
# PageVisit.objects.all().delete()

print("Generating dummy page views...")

end_date = timezone.now()
start_date = end_date - timedelta(days=60)
current_date = start_date

paths = ['/', '/blog/', '/projects/', '/about/', '/contact/']

while current_date <= end_date:
    # Random number of visits per day (between 10 and 100)
    num_visits = random.randint(10, 100)
    
    for _ in range(num_visits):
        # Random time within the day
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        visit_time = current_date.replace(hour=hour, minute=minute, second=second)
        
        PageVisit.objects.create(
            path=random.choice(paths),
            timestamp=visit_time,
            ip_address=f"192.168.1.{random.randint(1, 255)}",
            user_agent="Mozilla/5.0 (Dummy Agent)"
        )
    
    current_date += timedelta(days=1)

print(f"Successfully populated page views from {start_date.date()} to {end_date.date()}.")
