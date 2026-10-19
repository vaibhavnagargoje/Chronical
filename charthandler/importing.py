"""
Shared helpers for the chart data / chart template management commands.

Every command is scoped to one home.State (default: Maharashtra) via --state:
  - imports read from <BASE_DIR>/<State.name>/<chapter folder>/
  - every imported row is stamped with that state
  - --clear only deletes that state's rows
"""
from django.core.management.base import CommandError

from charthandler.chapters import DEFAULT_STATE_SLUG
from home.models import State


class StateScopedCommandMixin:
    """Mixin for BaseCommand subclasses that work on one state's data."""

    state = None

    def add_state_argument(self, parser):
        parser.add_argument(
            '--state',
            default=DEFAULT_STATE_SLUG,
            help=f'Slug of the home.State this data belongs to (default: {DEFAULT_STATE_SLUG})',
        )

    def resolve_state(self, options):
        try:
            self.state = State.objects.get(slug=options['state'])
        except State.DoesNotExist:
            raise CommandError(
                f"State with slug '{options['state']}' not found. Create it in the admin first."
            )
        self.stdout.write(f'State: {self.state.name}')
        return self.state

    def with_state(self, records):
        """
        Stamp every unsaved record with the command's state.

        Required before bulk_create(ignore_conflicts=True): on MySQL that becomes
        INSERT IGNORE, so a row without a state would be dropped silently.
        """
        if self.state is None:
            raise CommandError('resolve_state() must be called before importing records.')
        for record in records:
            record.state = self.state
        return records
