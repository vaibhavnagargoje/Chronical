from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Migrate Local Politics chapters from culture to statistic app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it',
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm you want to proceed with the actual migration',
        )

    def handle(self, *args, **options):
        # Import here to avoid circular imports
        from culture.models import CulturalChapter
        from statistic.models import StatisticalChapter
        
        # Safety check - ensure Local Politics is in statistic choices
        stat_choices = dict(StatisticalChapter.CHAPTER_CHOICES)
        if 'Local Politics' not in stat_choices:
            self.stdout.write(
                self.style.ERROR(
                    'ERROR: "Local Politics" not found in StatisticalChapter.CHAPTER_CHOICES. '
                    'Please add it first!'
                )
            )
            return
        
        # Find chapters to migrate
        local_politics_chapters = CulturalChapter.objects.filter(name='Local Politics')
        
        if not local_politics_chapters.exists():
            self.stdout.write(self.style.WARNING('No Local Politics chapters found in culture app.'))
            return
        
        self.stdout.write(f"Found {local_politics_chapters.count()} Local Politics chapters:")
        for chapter in local_politics_chapters:
            block_count = chapter.content_blocks.count()
            self.stdout.write(f"  - {chapter.district.name}, {chapter.district.state.name} ({block_count} content blocks)")
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes made'))
            self.show_detailed_preview(local_politics_chapters)
            return
        
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR(
                    'This will modify your database. Add --confirm flag to proceed, or --dry-run to preview.'
                )
            )
            return
        
        # Perform actual migration
        self.perform_migration(local_politics_chapters)

    def show_detailed_preview(self, chapters):
        """Show detailed preview of what will be migrated"""
        for chapter in chapters:
            self.stdout.write(f"\nChapter: {chapter}")
            self.stdout.write(f"District: {chapter.district.name}, {chapter.district.state.name}")
            self.stdout.write(f"Slug: {chapter.slug}")
            self.stdout.write(f"Updated: {chapter.updated_at}")
            
            blocks = chapter.content_blocks.all().order_by('order')
            self.stdout.write(f"Content blocks ({blocks.count()}):")
            
            for block in blocks:
                real_block = block.get_real_instance()
                block_type = type(real_block).__name__
                
                if hasattr(real_block, 'text'):
                    preview = real_block.text[:50] + "..." if len(real_block.text) > 50 else real_block.text
                elif hasattr(real_block, 'content'):
                    # Strip HTML tags for preview
                    import re
                    clean_content = re.sub('<[^<]+?>', '', str(real_block.content))
                    preview = clean_content[:50] + "..." if len(clean_content) > 50 else clean_content
                elif hasattr(real_block, 'caption'):
                    preview = real_block.caption or "No caption"
                elif hasattr(real_block, 'title'):
                    preview = real_block.title or "No title"
                else:
                    preview = "No preview available"
                
                self.stdout.write(f"  #{block.order} {block_type}: {preview}")

    def perform_migration(self, chapters):
        """Perform the actual migration"""
        from culture.models import CulturalChapter
        from statistic.models import StatisticalChapter
        
        migrated_count = 0
        
        with transaction.atomic():
            for cultural_chapter in chapters:
                self.stdout.write(f"\nMigrating: {cultural_chapter}")
                
                # Check if statistical chapter already exists
                existing_stat_chapter = StatisticalChapter.objects.filter(
                    district=cultural_chapter.district,
                    name='Local Politics'
                ).first()
                
                if existing_stat_chapter:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Statistical chapter already exists for {cultural_chapter.district.name}. Skipping."
                        )
                    )
                    continue
                
                # Create new statistical chapter
                stat_chapter = StatisticalChapter.objects.create(
                    district=cultural_chapter.district,
                    name='Local Politics',
                    slug=cultural_chapter.slug,
                    updated_at=cultural_chapter.updated_at or timezone.now()
                )
                
                self.stdout.write(f"Created statistical chapter: {stat_chapter}")
                
                # Migrate content blocks
                content_blocks = cultural_chapter.content_blocks.all().order_by('order')
                migrated_blocks = 0
                
                for block in content_blocks:
                    try:
                        self.migrate_content_block(block, stat_chapter)
                        migrated_blocks += 1
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"Error migrating block {block.id}: {str(e)}")
                        )
                        raise  # Re-raise to trigger rollback
                
                self.stdout.write(f"Migrated {migrated_blocks} content blocks")
                migrated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully migrated {migrated_count} chapters')
        )
        self.stdout.write(
            self.style.WARNING(
                'IMPORTANT: Verify the migration was successful before deleting the original cultural chapters!'
            )
        )

    def migrate_content_block(self, block, new_chapter):
        """Migrate a single content block to the new statistical chapter"""
        from culture.models import (
            HeadingBlockOne, HeadingBlockTwo, HeadingBlockThree,
            ParagraphBlock, ImageBlock, ReferenceBlock, ChartBlock
        )
        from statistic.models import (
            HeadingBlockOne as StatHeadingBlockOne,
            HeadingBlockTwo as StatHeadingBlockTwo, 
            HeadingBlockThree as StatHeadingBlockThree,
            ParagraphBlock as StatParagraphBlock, 
            ImageBlock as StatImageBlock,
            ReferenceBlock as StatReferenceBlock, 
            ChartBlock as StatChartBlock
        )
        
        # Get the actual polymorphic instance
        actual_block = block.get_real_instance()
        
        # Create the corresponding block in statistic app
        if isinstance(actual_block, HeadingBlockOne):
            new_block = StatHeadingBlockOne.objects.create(
                chapter=new_chapter,
                order=actual_block.order,
                text=actual_block.text
            )
        elif isinstance(actual_block, HeadingBlockTwo):
            new_block = StatHeadingBlockTwo.objects.create(
                chapter=new_chapter,
                order=actual_block.order,
                text=actual_block.text
            )
        elif isinstance(actual_block, HeadingBlockThree):
            new_block = StatHeadingBlockThree.objects.create(
                chapter=new_chapter,
                order=actual_block.order,
                text=actual_block.text
            )
        elif isinstance(actual_block, ParagraphBlock):
            new_block = StatParagraphBlock.objects.create(
                chapter=new_chapter,
                order=actual_block.order,
                content=actual_block.content
            )
        elif isinstance(actual_block, ImageBlock):
            new_block = StatImageBlock.objects.create(
                chapter=new_chapter,
                order=actual_block.order,
                image=actual_block.image,
                caption=actual_block.caption,
                alt_text=actual_block.alt_text,
                img_ref=getattr(actual_block, 'img_ref', '')
            )
        elif isinstance(actual_block, ReferenceBlock):
            new_block = StatReferenceBlock.objects.create(
                chapter=new_chapter,
                order=actual_block.order,
                text=actual_block.text,
                link=actual_block.link
            )
        elif isinstance(actual_block, ChartBlock):
            new_block = StatChartBlock.objects.create(
                chapter=new_chapter,
                order=actual_block.order,
                title=getattr(actual_block, 'title', ''),
                chart_html_file=actual_block.chart_html_file
            )
        else:
            raise ValueError(f"Unknown block type: {type(actual_block)}")
        
        self.stdout.write(f"  Migrated {type(actual_block).__name__} (order: {actual_block.order})")
        return new_block