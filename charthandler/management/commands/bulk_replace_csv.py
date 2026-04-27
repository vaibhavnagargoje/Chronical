import os
import glob
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Bulk replace text in all CSV files in a specified directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Livestocks'),
            help='Path to the directory containing CSV files'
        )
        parser.add_argument(
            '--old-text',
            type=str,
            required=True,
            help='Text to find'
        )
        parser.add_argument(
            '--new-text',
            type=str,
            required=True,
            help='Text to replace it with'
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        old_text = options['old_text']
        new_text = options['new_text']

        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f'Data directory not found: {data_dir}'))
            return

        self.stdout.write(f"Scanning CSV files in: {data_dir}")
        self.stdout.write(f"Replacing '{old_text}' with '{new_text}'")
        
        csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

        if not csv_files:
            self.stdout.write(self.style.WARNING("No CSV files found in the specified directory."))
            return

        for filepath in csv_files:
            try:
                # Read using utf-8-sig to handle special characters properly
                with open(filepath, 'r', encoding='utf-8-sig') as file:
                    content = file.read()
                    
                if old_text in content:
                    updated_content = content.replace(old_text, new_text)
                    
                    with open(filepath, 'w', encoding='utf-8-sig') as file:
                        file.write(updated_content)
                    
                    self.stdout.write(self.style.SUCCESS(f'[OK] Updated: {os.path.basename(filepath)}'))
                else:
                    self.stdout.write(f'[-] No changes needed in: {os.path.basename(filepath)}')
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] Error processing {os.path.basename(filepath)}: {e}'))

        self.stdout.write(self.style.SUCCESS('\nFinished processing all files.'))
