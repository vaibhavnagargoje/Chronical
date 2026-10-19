"""
Assign a state to every chart data row and chart template that has none.

One-time backfill used while introducing state scoping: existing data was all
Maharashtra, so every row with state = NULL gets Maharashtra.

Usage:
    python manage.py assign_default_state --dry-run     # report only
    python manage.py assign_default_state               # backfill (default: maharashtra)
    python manage.py assign_default_state --check       # fail if any NULL state remains
"""
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Count

from charthandler.chapters import DEFAULT_STATE_SLUG
from charthandler.models import ChartTemplate, StateScopedData
from home.models import State


def state_scoped_models():
    """Every charthandler model that carries a `state` FK (all data models + ChartTemplate)."""
    data_models = [
        model for model in apps.get_app_config('charthandler').get_models()
        if issubclass(model, StateScopedData)
    ]
    return data_models + [ChartTemplate]


class Command(BaseCommand):
    help = 'Backfill state on chart data rows and chart templates where it is NULL.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--state',
            default=DEFAULT_STATE_SLUG,
            help=f'Slug of the home.State to assign (default: {DEFAULT_STATE_SLUG})',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Only report how many rows would be updated',
        )
        parser.add_argument(
            '--check',
            action='store_true',
            help='Exit with an error if any row still has no state (no changes made)',
        )

    def handle(self, *args, **options):
        models_to_fill = state_scoped_models()

        if options['check']:
            self._check(models_to_fill)
            return

        try:
            state = State.objects.get(slug=options['state'])
        except State.DoesNotExist:
            raise CommandError(
                f"State with slug '{options['state']}' not found. Create it in the admin first."
            )

        self._abort_on_duplicate_templates()

        dry_run = options['dry_run']
        self.stdout.write(
            f"{'[DRY RUN] ' if dry_run else ''}Assigning state '{state.name}' "
            f"to rows with no state across {len(models_to_fill)} models..."
        )

        total = 0
        with transaction.atomic():
            for model in models_to_fill:
                pending = model.objects.filter(state__isnull=True)
                count = pending.count() if dry_run else pending.update(state=state)
                if count:
                    self.stdout.write(f'  {model.__name__}: {count}')
                total += count

        self.stdout.write(self.style.SUCCESS(
            f"\n{'Would update' if dry_run else 'Updated'} {total} rows."
        ))

    def _abort_on_duplicate_templates(self):
        # (state, chapter_type, title) becomes unique — existing duplicates would block that migration.
        duplicates = (
            ChartTemplate.objects
            .values('chapter_type', 'title')
            .annotate(n=Count('id'))
            .filter(n__gt=1)
        )
        if duplicates:
            lines = '\n'.join(
                f"  - [{d['chapter_type']}] {d['title']} (x{d['n']})" for d in duplicates
            )
            raise CommandError(
                'Duplicate chart templates (same chapter_type + title) must be resolved first:\n' + lines
            )

    def _check(self, models_to_fill):
        missing = {}
        for model in models_to_fill:
            count = model.objects.filter(state__isnull=True).count()
            if count:
                missing[model.__name__] = count

        if missing:
            lines = '\n'.join(f'  {name}: {count}' for name, count in missing.items())
            raise CommandError(f'Rows without a state remain:\n{lines}')

        self.stdout.write(self.style.SUCCESS(
            f'OK: every row in {len(models_to_fill)} models has a state.'
        ))
