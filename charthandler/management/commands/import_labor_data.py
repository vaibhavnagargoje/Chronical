"""
Management command to import labor CSV data into the database.

Usage:
    python manage.py import_labor_data [--data-dir PATH] [--clear]

Default data directory: Labor/ in the project root.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.apps import apps


def _safe_float(value):
    if value is None or str(value).strip() == '':
        return None
    try:
        return float(str(value).strip())
    except (ValueError, TypeError):
        return None


# Each entry: csv_filename -> (app_label.ModelName, {csv_header: model_field})
# Fields 'district' and 'year' are handled automatically.
CSV_MAP = {
    'labor_workers.csv': ('charthandler.LaborWorkers', {
        'Rural/Urban': 'rural_urban',
        'Male Main Workers': 'male_main_workers',
        'Female Main Workers': 'female_main_workers',
        'Male Marginal Workers': 'male_marginal_workers',
        'Female Marginal Workers': 'female_marginal_workers',
    }),
    'labor_age_distribution.csv': ('charthandler.LaborAgeDistribution', {
        'Rural/Urban': 'rural_urban',
        'Age Group': 'age_group',
        'Main Workers': 'main_workers',
        'Marginal Workers': 'marginal_workers',
        'Non Workers': 'non_workers',
    }),
    'labor_ec_workers.csv': ('charthandler.LaborECWorkers', {
        'Number of Workers': 'number_of_workers',
        'Number of Establishments': 'number_of_establishments',
        'Govt/PSU Workers': 'govt_psu_workers',
        'Cooperative Workers': 'cooperative_workers',
        'Private Sector Workers': 'private_sector_workers',
    }),
    'labor_ec_gender.csv': ('charthandler.LaborECGender', {
        'Gender': 'gender',
        'Employed Hired': 'employed_hired',
        'Employed Not Hired': 'employed_not_hired',
    }),
    'labor_ec_religion.csv': ('charthandler.LaborECReligion', {
        'Religion': 'religion',
        'Number of Establishments': 'number_of_establishments',
    }),
    'labor_mnrega_job_cards.csv': ('charthandler.LaborMNREGAJobCards', {
        'Job Cards Issued': 'job_cards_issued',
        'SC': 'sc',
        'ST': 'st',
        'Issued for SC or ST': 'issued_for_sc_or_st',
    }),
    'labor_mnrega_participation.csv': ('charthandler.LaborMNREGAParticipation', {
        'Worked': 'worked',
        'Demanded Work': 'demanded_work',
        'Allotted Work': 'allotted_work',
    }),
    'labor_mnrega_accounts.csv': ('charthandler.LaborMNREGAAccounts', {
        'Bank Accounts': 'bank_accounts',
        'Post Office Accounts': 'post_office_accounts',
    }),
    'labor_mnrega_scope.csv': ('charthandler.LaborMNREGAScope', {
        'Worked': 'worked',
        'Demanded Work': 'demanded_work',
        'Allotted Work': 'allotted_work',
    }),
    'labor_govt_employees.csv': ('charthandler.LaborGovtEmployees', {
        'Group': 'group',
        'Approved Posts': 'approved_posts',
        'Positions Filled': 'positions_filled',
        'Number of Women': 'number_of_women',
    }),
    'labor_dsa_establishments.csv': ('charthandler.LaborDSAEstablishments', {
        'Taluka': 'taluka',
        'Shops': 'shops',
        'Business Organizations': 'business_organizations',
        'Hotels and Restaurants': 'hotels_and_restaurants',
        'Cinema Halls': 'cinema_halls',
        'Organizations without Workers': 'organizations_without_workers',
    }),
    'labor_dsa_workers.csv': ('charthandler.LaborDSAWorkers', {
        'Taluka': 'taluka',
        'Shops': 'shops',
        'Business Organizations': 'business_organizations',
        'Hotels and Restaurants': 'hotels_and_restaurants',
        'Cinema Halls': 'cinema_halls',
    }),
    'labor_industry_type.csv': ('charthandler.LaborIndustryType', {
        'Type of Industry': 'type_of_industry',
        'Govt Employees': 'govt_employees',
        'Semi Govt Employees': 'semi_govt_employees',
        'Private Employees': 'private_employees',
        'Total Employees': 'total_employees',
    }),
}

# Fields that are always strings, not floats
STRING_FIELDS = {
    'rural_urban', 'age_group', 'gender', 'religion', 'group', 'taluka', 'type_of_industry'
}

class Command(BaseCommand):
    help = 'Import labor CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir', type=str,
            default=os.path.join(settings.BASE_DIR, 'Labor'),
            help='Path to the directory containing labor CSV files',
        )
        parser.add_argument(
            '--clear', action='store_true',
            help='Clear existing labor data before importing',
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing from: {data_dir}')

        # Resolve all model classes
        model_cache = {}
        for csv_file, (model_path, _) in CSV_MAP.items():
            app_label, model_name = model_path.rsplit('.', 1)
            model_cache[csv_file] = apps.get_model(app_label, model_name)

        if options['clear']:
            self.stdout.write('Clearing existing labor data...')
            for csv_file, ModelClass in model_cache.items():
                ModelClass.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        for csv_file, (model_path, col_map) in CSV_MAP.items():
            filepath = os.path.join(data_dir, csv_file)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'  [SKIP] {csv_file} (Not found)'))
                continue

            ModelClass = model_cache[csv_file]
            try:
                count = self._import_csv(filepath, ModelClass, col_map)
                self.stdout.write(self.style.SUCCESS(f'  [OK] {csv_file} — {count} records'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [ERROR] {csv_file}: {e}'))

        self.stdout.write(self.style.SUCCESS('\\nImport complete!'))

    def _import_csv(self, filepath, ModelClass, col_map):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                kwargs = {}
                
                # Handling district
                kwargs['district'] = row.get('District', '').strip()

                # Handling year
                year = row.get('Year')
                if year is not None and str(year).strip() != '':
                    year_val = _safe_float(year)
                    if year_val is not None:
                        kwargs['year'] = int(year_val)
                    else:
                        kwargs['year'] = None
                else:
                    # In case year column is completely missing or empty (e.g., labor_ec_religion)
                    if ModelClass.__name__ == 'LaborECReligion':
                        kwargs['year'] = 2013
                    else:
                        kwargs['year'] = None
                
                # Make sure the model accepts null year if year is missing
                # Some models might fail validation if year is required but missing,
                # but we defined LaborECReligion with null=True for year.

                # Skip if model requires year
                if kwargs.get('year') is None and ModelClass.__name__ != 'LaborECReligion':
                    continue

                for csv_col, model_field in col_map.items():
                    raw = row.get(csv_col, '')
                    if model_field in STRING_FIELDS:
                        kwargs[model_field] = str(raw).strip() if raw else ''
                    else:
                        kwargs[model_field] = _safe_float(raw)

                records.append(ModelClass(**kwargs))

        ModelClass.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
