"""
Management command to import industry CSV data into the database.

Usage:
    python manage.py import_industry_data [--data-dir PATH]

Default data directory: Industry/ in the project root.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from charthandler.models import (
    ECNumber,
    ECSocialGroup,
    ECSourcesOfFinance,
    ECSourcesOfBorrowings,
    ECType,
    ECBroadActivity,
    DSAMsme,
    FactoryWorkers,
    DSAElectricity,
    DSAPollutionCategory,
)


def _safe_float(value):
    """Safely convert a string to float, returning None for empty/invalid."""
    if value is None or str(value).strip() == '':
        return None
    try:
        return float(str(value).strip().replace(',', ''))
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    """Safely convert a string to int, returning None for empty/invalid."""
    f = _safe_float(value)
    if f is None:
        return None
    return int(f)


class Command(BaseCommand):
    help = 'Import industry CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Industry'),
            help='Path to the directory containing industry CSV files'
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
            self.stdout.write('Clearing existing industry data...')
            ECNumber.objects.all().delete()
            ECSocialGroup.objects.all().delete()
            ECSourcesOfFinance.objects.all().delete()
            ECSourcesOfBorrowings.objects.all().delete()
            ECType.objects.all().delete()
            ECBroadActivity.objects.all().delete()
            DSAMsme.objects.all().delete()
            FactoryWorkers.objects.all().delete()
            DSAElectricity.objects.all().delete()
            DSAPollutionCategory.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        csv_files = {
            'ec_number.csv': self._import_ec_number,
            'ec_social_group.csv': self._import_ec_social_group,
            'ec_sources_of_finance.csv': self._import_ec_sources_of_finance,
            'ec_sources_of_borrowings.csv': self._import_ec_sources_of_borrowings,
            'ec_type.csv': self._import_ec_type,
            'ec_broad_activity.csv': self._import_ec_broad_activity,
            'dsa_msme.csv': self._import_dsa_msme,
            'mahadish_factory_workers.csv': self._import_factory_workers,
            'dsa_electricity.csv': self._import_dsa_electricity,
            'dsa_pollution_cat.csv': self._import_dsa_pollution_cat,
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

    # -------------------------------------------------------------------------

    def _import_ec_number(self, filepath):
        """Import ec_number.csv → ECNumber"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(ECNumber(
                    year=year,
                    district=row.get('District', '').strip(),
                    number_of_establishments=_safe_float(row.get('Number of Establishments')),
                ))
        ECNumber.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ec_social_group(self, filepath):
        """Import ec_social_group.csv → ECSocialGroup"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(ECSocialGroup(
                    year=year,
                    district=row.get('District', '').strip(),
                    sc=_safe_float(row.get('SC')),
                    st=_safe_float(row.get('ST')),
                    obc=_safe_float(row.get('OBC')),
                    others=_safe_float(row.get('Others')),
                ))
        ECSocialGroup.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ec_sources_of_finance(self, filepath):
        """Import ec_sources_of_finance.csv → ECSourcesOfFinance"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(ECSourcesOfFinance(
                    year=year,
                    district=row.get('District', '').strip(),
                    self_financed=_safe_float(row.get('Self-Financed')),
                    borrowings_and_other_assistance=_safe_float(row.get('Borrowings and Other Assistance')),
                ))
        ECSourcesOfFinance.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ec_sources_of_borrowings(self, filepath):
        """Import ec_sources_of_borrowings.csv → ECSourcesOfBorrowings"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(ECSourcesOfBorrowings(
                    year=year,
                    district=row.get('District', '').strip(),
                    self_financed=_safe_float(row.get('Self-Financed')),
                    borrowing_from_institutions=_safe_float(row.get('Borrowing from Institutions')),
                    borrowing_from_non_institutions=_safe_float(row.get('Borrowing from Non-Institutions')),
                    financial_assistance_from_govt=_safe_float(row.get('Financial Assistance from Govt. sources')),
                    loans_from_shgs=_safe_float(row.get('Loans from SHGs')),
                    donations_transfers=_safe_float(row.get('Donations/Transfers')),
                    others=_safe_float(row.get('Others')),
                ))
        ECSourcesOfBorrowings.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ec_type(self, filepath):
        """Import ec_type.csv → ECType"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(ECType(
                    year=year,
                    district=row.get('District', '').strip(),
                    govt_psu=_safe_float(row.get('Govt/PSU')),
                    cooperative=_safe_float(row.get('Cooperative')),
                    private_sector=_safe_float(row.get('Private Sector')),
                ))
        ECType.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ec_broad_activity(self, filepath):
        """Import ec_broad_activity.csv → ECBroadActivity"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(ECBroadActivity(
                    year=year,
                    district=row.get('District', '').strip(),
                    agriculture_and_allied_activities=_safe_float(row.get('Agriculture and Allied Activities')),
                    industry=_safe_float(row.get('Industry')),
                    services=_safe_float(row.get('Services')),
                ))
        ECBroadActivity.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_msme(self, filepath):
        """Import dsa_msme.csv → DSAMsme"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DSAMsme(
                    district=row.get('District', '').strip(),
                    year=year,
                    taluka=row.get('Taluka', '').strip(),
                    number_of_msme_industries=_safe_float(row.get('Number of MSME Industries')),
                ))
        DSAMsme.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_factory_workers(self, filepath):
        """Import mahadish_factory_workers.csv → FactoryWorkers (aggregated per taluka+category)"""
        from collections import defaultdict
        # Aggregate workers: same district+year+taluka+category can have multiple rows → sum them
        agg = defaultdict(float)
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                key = (
                    row.get('District', '').strip(),
                    year,
                    row.get('Taluka', '').strip(),
                    row.get('Manufacturing Category', '').strip(),
                )
                workers = _safe_float(row.get('No. of Workers')) or 0
                agg[key] += workers

        records = [
            FactoryWorkers(
                district=k[0],
                year=k[1],
                taluka=k[2],
                manufacturing_category=k[3],
                num_workers=v,
            )
            for k, v in agg.items()
        ]
        FactoryWorkers.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_electricity(self, filepath):
        """Import dsa_electricity.csv → DSAElectricity"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DSAElectricity(
                    district=row.get('District', '').strip(),
                    year=year,
                    taluka=row.get('Taluka', '').strip(),
                    industrial_power_consumption=_safe_float(row.get('Industrial Power Consumption')),
                ))
        DSAElectricity.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_pollution_cat(self, filepath):
        """Import dsa_pollution_cat.csv → DSAPollutionCategory"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DSAPollutionCategory(
                    district=row.get('District', '').strip(),
                    year=year,
                    taluka=row.get('Taluka', '').strip(),
                    pollution_category=row.get('Pollution Category ', '').strip(),
                    number_of_industries=_safe_float(row.get('Number of Industries ')),
                ))
        DSAPollutionCategory.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
