import urllib.request
import json
from django.core.management.base import BaseCommand
from blog.models import Project

class Command(BaseCommand):
    help = 'Fetches repositories from GitHub and updates the Project model'

    def handle(self, *args, **kwargs):
        github_api_url = 'https://api.github.com/users/badalaryal11/repos?sort=updated&per_page=100'
        
        self.stdout.write("Fetching repositories from GitHub...")
        
        try:
            req = urllib.request.Request(
                github_api_url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            response = urllib.request.urlopen(req)
            repos = json.loads(response.read())
            
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
                        'image_url': self.get_image_for_language(language)
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Imported: {name}"))
                else:
                    # Update existing records
                    obj.description = description
                    obj.link = html_url
                    obj.tech_stack = language
                    obj.image_url = self.get_image_for_language(language)
                    obj.save()
                    self.stdout.write(f"Updated: {name}")
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

    def get_image_for_language(self, language):
        # Simple mapping for placeholder images based on language
        base_url = "https://ui-avatars.com/api/?background=random&color=fff&size=500&name="
        if not language:
            return base_url + "Code"
        return base_url + language
