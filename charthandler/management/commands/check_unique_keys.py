"""
Compare charthandler's unique_together keys in the applied migration state
with the unique keys that actually exist in the database.

Migrations that change unique_together first drop the old key and fail with
"Found wrong number (0) of constraints" when the database never had it.
Run this before such a migration (e.g. the state-scoping migration):

    python manage.py check_unique_keys          # report only
    python manage.py check_unique_keys --fix    # create missing keys (refuses tables with duplicates)
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.migrations.loader import MigrationLoader


APP_LABEL = 'charthandler'


def applied_project_state():
    """Project state as of the migrations actually applied to this database."""
    loader = MigrationLoader(connection)
    applied = set(loader.applied_migrations)
    leaves = [
        node for node in applied
        if node in loader.graph.node_map
        and not any(child in applied for child in loader.graph.node_map[node].children)
    ]
    return loader.project_state(nodes=leaves, at_end=True)


class Command(BaseCommand):
    help = "Report (and with --fix, create) unique_together keys missing from charthandler tables."

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Create missing unique keys (tables with duplicate rows are skipped and reported)',
        )

    def handle(self, *args, **options):
        state_apps = applied_project_state().apps
        missing, extra = [], []

        with connection.cursor() as cursor:
            for model in state_apps.get_app_config(APP_LABEL).get_models():
                table = model._meta.db_table
                expected = {
                    tuple(model._meta.get_field(name).column for name in fields): fields
                    for fields in model._meta.unique_together
                }
                actual = {
                    tuple(info['columns'])
                    for info in connection.introspection.get_constraints(cursor, table).values()
                    if info['unique'] and not info['primary_key'] and len(info['columns']) > 1
                }
                for columns, fields in expected.items():
                    if columns not in actual:
                        missing.append((model, columns, fields))
                for columns in actual - set(expected):
                    extra.append((table, columns))

        if extra:
            self.stdout.write(self.style.WARNING('Unique keys in the database that the migrations do not know about:'))
            for table, columns in extra:
                self.stdout.write(f'  {table} {columns}')

        if not missing:
            self.stdout.write(self.style.SUCCESS('OK: every unique_together key exists in the database.'))
            return

        self.stdout.write(self.style.WARNING('Unique keys expected by the migrations but missing in the database:'))
        for model, columns, _ in missing:
            self.stdout.write(f'  {model._meta.db_table} {columns}')

        if not options['fix']:
            raise CommandError('Missing unique keys found. Re-run with --fix to create them.')

        failed = []
        for model, columns, fields in missing:
            duplicates = self._count_duplicate_groups(model._meta.db_table, columns)
            if duplicates:
                failed.append(f'{model._meta.db_table}: {duplicates} duplicate groups on {columns}')
                continue
            with connection.schema_editor() as schema_editor:
                schema_editor.alter_unique_together(model, set(), {fields})
            self.stdout.write(self.style.SUCCESS(f'  [CREATED] {model._meta.db_table} {columns}'))

        if failed:
            raise CommandError('Could not create keys (remove duplicate rows first):\n  ' + '\n  '.join(failed))

    def _count_duplicate_groups(self, table, columns):
        qn = connection.ops.quote_name
        cols = ', '.join(qn(c) for c in columns)
        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT COUNT(*) FROM (SELECT 1 FROM {qn(table)} GROUP BY {cols} HAVING COUNT(*) > 1) d'
            )
            return cursor.fetchone()[0]
