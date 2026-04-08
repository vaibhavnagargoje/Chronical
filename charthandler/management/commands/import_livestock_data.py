"""
Management command to import livestock CSV data into the database.

Usage:
    python manage.py import_livestock_data [--data-dir PATH]

Default data directory: Livestocks/ in the project root.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from charthandler.models import (
    LivestockNumbers,
    ArtificialInsemination,
    DairyCooperative,
    DairyByproduct,
    Fisheries,
    Veterinary,
)


def _safe_float(value):
    """Safely convert a string to float, returning None for empty/invalid."""
    if value is None or value == '' or value.strip() == '':
        return None
    try:
        return float(value.strip())
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    """Safely convert a string to int, returning None for empty/invalid."""
    f = _safe_float(value)
    if f is None:
        return None
    return int(f)


class Command(BaseCommand):
    help = 'Import livestock CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Livestocks'),
            help='Path to the directory containing livestock CSV files'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before importing'
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        clear = options['clear']

        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing from: {data_dir}')

        if clear:
            self.stdout.write('Clearing existing data...')
            LivestockNumbers.objects.all().delete()
            ArtificialInsemination.objects.all().delete()
            DairyCooperative.objects.all().delete()
            DairyByproduct.objects.all().delete()
            Fisheries.objects.all().delete()
            Veterinary.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # Import each CSV file
        csv_files = {
            'number_of_livestock_(dsa).csv': self._import_livestock_numbers,
            'artificial_insemination_(dsa).csv': self._import_artificial_insemination,
            'dairy_co-op_(dsa).csv': self._import_dairy_cooperative,
            'dairy_byproducts_(dsa)_(not_gra.csv': self._import_dairy_byproducts,
            'fisheries_(dsa).csv': self._import_fisheries,
            'veterinary_(dsa).csv': self._import_veterinary,
        }

        for filename, importer in csv_files.items():
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                self.stdout.write(f'\nImporting {filename}...')
                try:
                    count = importer(filepath)
                    self.stdout.write(self.style.SUCCESS(f'  [OK] {count} records imported'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  [ERROR] {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [SKIP] File not found: {filename}'))

        self.stdout.write(self.style.SUCCESS('\nImport complete!'))

    def _import_livestock_numbers(self, filepath):
        """Import number_of_livestock_(dsa).csv"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_float(row.get('Year'))
                if year is None:
                    continue
                records.append(LivestockNumbers(
                    district=row.get('District', '').strip(),
                    year=int(year),
                    hybrid_cows=_safe_float(row.get('Hybrid Cows')),
                    native_cows=_safe_float(row.get('Native Cows')),
                    buffalo=_safe_float(row.get('Buffalo')),
                ))

        LivestockNumbers.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_artificial_insemination(self, filepath):
        """Import artificial_insemination_(dsa).csv"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_float(row.get('Year'))
                if year is None:
                    continue
                records.append(ArtificialInsemination(
                    district=row.get('District', '').strip(),
                    year=int(year),
                    taluka=row.get('Taluka', '').strip(),
                    annual_target=_safe_float(row.get('Annual Target for Artificial Insemination')),
                    actual_numbers=_safe_float(row.get('Actual Artificial Insemination Numbers')),
                    percentage_achieved=_safe_float(row.get('Percentage of Artificial Insemination Target Achieved')),
                ))

        ArtificialInsemination.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dairy_cooperative(self, filepath):
        """Import dairy_co-op_(dsa).csv"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_float(row.get('Year'))
                if year is None:
                    continue
                records.append(DairyCooperative(
                    district=row.get('District', '').strip(),
                    year=int(year),
                    taluka=row.get('Taluka', '').strip(),
                    cooperative_societies=_safe_float(row.get('Dairy Development Cooperative Societies')),
                    memberships=_safe_float(row.get('Memberships in Dairy Co-op Societies')),
                    milk_collected_annually=_safe_float(row.get('Milk collected across the year')),
                    avg_milk_per_day=_safe_float(row.get('Average milk collected per day')),
                    cold_storage_units=_safe_float(row.get('Number of cold storage units')),
                    cold_storage_capacity=_safe_float(row.get('Cold Storage Capacity')),
                ))

        DairyCooperative.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dairy_byproducts(self, filepath):
        """Import dairy_byproducts_(dsa)_(not_gra.csv"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_float(row.get('Year'))
                if year is None:
                    continue
                item = row.get('Items', '').strip()
                if not item:
                    continue
                records.append(DairyByproduct(
                    district=row.get('District', '').strip(),
                    year=int(year),
                    item=item,
                    units=_safe_float(row.get('Units')),
                ))

        DairyByproduct.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_fisheries(self, filepath):
        """Import fisheries_(dsa).csv"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_float(row.get('Year'))
                if year is None:
                    continue
                records.append(Fisheries(
                    district=row.get('District', '').strip(),
                    year=int(year),
                    taluka=row.get('Taluka', '').strip(),
                    length_of_rivers=_safe_float(row.get('Length of Rivers')),
                    num_lakes_ponds_reservoirs=_safe_float(row.get('Number of Lakes, Ponds or Reservoirs Suitable for Fishing')),
                    area_suitable_for_fishing=_safe_float(row.get('Area Suitable for Fishing')),
                    area_used_for_commercial_fisheries=_safe_float(row.get('Area Used for Commercial Fisheries')),
                    groundwater_fish_production=_safe_float(row.get('Groundwater Fish Production')),
                    price_received_by_producers=_safe_float(row.get('Price Received by Producers for Fish Caught')),
                    fish_seeds_used=_safe_float(row.get('Fish Seeds Used')),
                    fish_business_cooperatives=_safe_float(row.get('Fish Business Cooperatives')),
                    members_in_cooperatives=_safe_float(row.get('Members in Fish Business Cooperatives')),
                ))

        Fisheries.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_veterinary(self, filepath):
        """Import veterinary_(dsa).csv"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_float(row.get('Year'))
                if year is None:
                    continue
                records.append(Veterinary(
                    district=row.get('District', '').strip(),
                    year=int(year),
                    taluka=row.get('Taluka', '').strip(),
                    veterinary_hospitals=_safe_int(row.get('Veterinary Hospitals')),
                    first_aid_centres=_safe_int(row.get('Veterinary First-Aid Centres')),
                    other_facilities=_safe_int(row.get('Other Veterinary Facilities')),
                    total_facilities=_safe_int(row.get('Total Veterinary Facilities')),
                ))

        Veterinary.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
