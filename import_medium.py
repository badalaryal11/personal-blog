import os
import django
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from blog.models import BlogPost

RSS_URL = 'https://medium.com/feed/@badalaryal'

def fetch_rss():
    req = urllib.request.Request(
        RSS_URL, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    response = urllib.request.urlopen(req)
    return response.read()

def parse_and_save(xml_data):
    root = ET.fromstring(xml_data)
    channel = root.find('channel')
    
    # Namespaces
    namespaces = {
        'content': 'http://purl.org/rss/1.0/modules/content/'
    }
    
    for item in channel.findall('item'):
        title = item.find('title').text
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
                'image_url': image_url
            }
        )
        
        if created:
            print(f"Imported: {title}")
        else:
            print(f"Skipped (exists): {title}")

if __name__ == '__main__':
    print("Fetching RSS feed...")
    try:
        xml_data = fetch_rss()
        print("Parsing and saving...")
        parse_and_save(xml_data)
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
