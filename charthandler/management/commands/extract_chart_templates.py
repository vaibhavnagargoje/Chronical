"""
DEPRECATED: This command has been split into two separate management commands:
1. extract_livestock_templates
2. extract_agriculture_templates
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'DEPRECATED: Please use extract_livestock_templates and extract_agriculture_templates instead.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'WARNING: This command is deprecated and has been split for modularity.\n\n'
            'To extract templates, please run the specific commands:\n'
            '--------------------------------------------------------\n'
            '  python manage.py extract_livestock_templates\n'
            '  python manage.py extract_agriculture_templates\n'
        ))
