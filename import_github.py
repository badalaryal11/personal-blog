import os
import django
import urllib.request
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from blog.models import Project

GITHUB_API_URL = 'https://api.github.com/users/badalaryal11/repos?sort=updated&per_page=100'

def fetch_repos():
    req = urllib.request.Request(
        GITHUB_API_URL, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0'
        }
    )
    response = urllib.request.urlopen(req)
    return json.loads(response.read())

def get_image_for_language(language):
    # Simple mapping for placeholder images based on language
    base_url = "https://ui-avatars.com/api/?background=random&color=fff&size=500&name="
    if not language:
        return base_url + "Code"
    return base_url + language

def import_projects():
    print("Fetching repositories from GitHub...")
    try:
        repos = fetch_repos()
        for repo in repos:
            if repo.get('fork'):
                continue
            
            name = repo.get('name')
            description = repo.get('description') or "No description available."
            html_url = repo.get('html_url')
            language = repo.get('language') or "Code"
            
            # Create or Update
            obj, created = Project.objects.get_or_create(
                title=name,
                defaults={
                    'description': description,
                    'link': html_url,
                    'tech_stack': language,
                    'image_url': get_image_for_language(language)
                }
            )
            
            if created:
                print(f"Imported: {name}")
            else:
                # Update existing if needed (optional, here just skipping)
                print(f"Skipped (exists): {name}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    import_projects()
