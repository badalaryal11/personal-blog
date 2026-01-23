import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
import re
from django.core.management.base import BaseCommand
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Fetches articles from Medium RSS feed and updates the BlogPost model'

    def handle(self, *args, **kwargs):
        rss_url = 'https://medium.com/feed/@badalaryal'
        
        self.stdout.write("Fetching RSS feed from Medium...")
        
        try:
            req = urllib.request.Request(
                rss_url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            response = urllib.request.urlopen(req)
            xml_data = response.read()
            
            root = ET.fromstring(xml_data)
            channel = root.find('channel')
            
            # Namespaces
            namespaces = {
                'content': 'http://purl.org/rss/1.0/modules/content/'
            }
            
            for item in channel.findall('item'):
                title = item.find('title').text
                link = item.find('link').text
                # pubDate
                pub_date_str = item.find('pubDate').text
                pub_date = parsedate_to_datetime(pub_date_str)
                
                # Content
                content_encoded = item.find('content:encoded', namespaces)
                content = content_encoded.text if content_encoded is not None else ''
                
                # Extract image
                image_url = ''
                img_match = re.search(r'<img[^>]+src="([^">]+)"', content)
                if img_match:
                    image_url = img_match.group(1)
                    
                # Create or Update
                obj, created = BlogPost.objects.get_or_create(
                    title=title,
                    defaults={
                        'content': content,
                        'date_posted': pub_date,
                        'image_url': image_url,
                        'canonical_url': link
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Imported: {title}"))
                else:
                    # Update existing records
                    obj.content = content
                    obj.date_posted = pub_date
                    obj.image_url = image_url
                    obj.canonical_url = link
                    obj.save()
                    self.stdout.write(f"Updated: {title}")
                        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
