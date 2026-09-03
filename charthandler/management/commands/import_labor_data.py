"""
Management command to import labor CSV data into the database.

Usage:
    python manage.py import_labor_data [--data-dir PATH] [--clear]

Default data directory: Labor/ in the project root.

All CSV files are sourced from MH_labour.xlsx (12 cleaned sheets).
Column names in CSV_MAP match exact headers in the generated CSVs.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.apps import apps


def _safe_float(value):
    if value is None or str(value).strip() in ('', 'nan', 'NaN', 'None'):
        return None
    try:
        return float(str(value).strip().replace(',', ''))
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    f = _safe_float(value)
    return int(f) if f is not None else None


# ─── CSV → (Model, {csv_col: model_field}, extra_flags) ──────────────────────
#
# Columns 'District' and 'Year' are handled automatically by _import_csv().
# '_no_year': True  → sheet has no Year column (skip year parsing entirely)
# '_year_first': True → Year column appears before District in CSV
#
CSV_MAP = {

    # ── Non Workers Yearly (5 cols) ───────────────────────────────────────────
    'labor_non_workers_yearly.csv': ('charthandler.LaborNonWorkersYearly', {
        'Rural/Urban':       'rural_urban',
        'Male Non Workers':  'male_non_workers',
        'Female Non Workers':'female_non_workers',
    }, {}),

    # ── Labour Working Populations (12 usable cols, 3 unnamed skipped) ────────
    'labor_working_populations.csv': ('charthandler.LaborWorkingPopulations', {
        'Rural/Urban':               'rural_urban',
        'Working Population':        'working_population',
        'Male Working Population':   'male_working_population',
        'Female Working Population': 'female_working_population',
        'Main Worker Population':    'main_worker_population',
        'Male Main Workers':         'male_main_workers',
        'Female Main Workers':       'female_main_workers',
        'Marginal Worker Population':'marginal_worker_population',
        'Male Marginal Workers':     'male_marginal_workers',
        'Female Marginal Workers':   'female_marginal_workers',
    }, {}),

    # ── Census Age Distribution (9 cols) ──────────────────────────────────────
    'labor_census_age_distribution.csv': ('charthandler.LaborCensusAgeDistribution', {
        'Rural/Urban':              'rural_urban',
        'Age Group':                'age_group',
        'Main Workers':             'main_workers',
        'Marginal Workers':         'marginal_workers',
        'Non-Workers':              'non_workers',
        'Non-Workers Seeking Work': 'non_workers_seeking_work',
        'People Seeking Work':      'people_seeking_work',
    }, {}),

    # ── Economic Census Workers (36 cols) ─────────────────────────────────────
    'labor_economic_census_workers.csv': ('charthandler.LaborEconomicCensusWorkers', {
        'Number of Workers':                                  'number_of_workers',
        'Number of Establishments':                           'number_of_establishments',
        'Houses used for Commercial Purposes':                'houses_commercial',
        'Houses used for Residential cum Commercial Purposes':'houses_residential_cum_commercial',
        'Govt / PSU':                                         'govt_psu',
        'Private Proprietary':                                'private_proprietary',
        'Private Partnership':                                'private_partnership',
        'Private Company':                                    'private_company',
        'Private Self Help Group':                            'private_self_help_group',
        'Co-operative':                                       'cooperative',
        'Private Non-profit Institution':                     'private_non_profit',
        'Private Other':                                      'private_other',
        'Private Sector':                                     'private_sector',
        'Self-Financed':                                      'self_financed',
        'Borrowing from Institutions':                        'borrowing_from_institutions',
        'Borrowing from Non-Institutions':                    'borrowing_from_non_institutions',
        '\xa0Financial Assistance from Govt. sources':        'financial_assistance_govt',
        'Loans from SHGs':                                    'loans_from_shgs',
        'Donations/Transfers':                                'donations_transfers',
        'Other SOF':                                          'other_sof',
        'Perennial':                                          'perennial',
        'Non-Perennial':                                      'non_perennial',
        'SC':                                                 'sc',
        'ST':                                                 'st',
        'OBC':                                                'obc',
        'Others':                                             'others_social',
        'Hindu':                                              'hindu',
        'Islam':                                              'islam',
        'Christian':                                          'christian',
        'Sikh':                                               'sikh',
        'Buddhist':                                           'buddhist',
        'Zoroastrian':                                        'zoroastrian',
        'Jain':                                               'jain',
        'Others.1':                                           'others_religion',
    }, {}),

    # ── Economic Census Gender (5 cols) ───────────────────────────────────────
    'labor_economic_census_gender.csv': ('charthandler.LaborEconomicCensusGender', {
        'Gender':               'gender',
        'Employed (Hired)':     'employed_hired',
        'Employed (Not Hired)': 'employed_not_hired',
    }, {}),

    # ── DSA MSME (6 cols) — District first, then Year ─────────────────────────
    'labor_dsa_msme.csv': ('charthandler.LaborDsaMsme', {
        'Taluka':                          'taluka',
        'Number of MSME Industries':       'number_of_msme_industries',
        'Number of employees (in Lakh)':   'number_of_employees_lakh',
        'Number of Employees':             'number_of_employees',
    }, {'_district_first': True}),

    # ── Employment by Industry (6 cols) — District first, then Year ───────────
    'labor_emp_by_industry.csv': ('charthandler.LaborEmpByIndustry', {
        'Select Industry':      'select_industry',
        'Govt. Employees':      'govt_employees',
        'Semi-Govt. Employees': 'semi_govt_employees',
        'Private Employees':    'private_employees',
    }, {'_district_first': True}),

    # ── Govt Employees (6 cols) — District first, then Year ───────────────────
    'labor_govt_employees.csv': ('charthandler.LaborGovtEmployees', {
        'Group':            'group',
        'Approved Posts':   'approved_posts',
        'Positions Filled': 'positions_filled',
        'Number of women':  'number_of_women',
    }, {'_district_first': True}),

    # ── MNREGA Accounts (4 cols) — District first, then Year ──────────────────
    'labor_mnrega_accounts.csv': ('charthandler.LaborMNREGAAccounts', {
        'Bank Accounts':        'bank_accounts',
        'Post Office Accounts': 'post_office_accounts',
    }, {'_district_first': True}),

    # ── MNREGA Job Cards (6 cols) — District first, then Year ─────────────────
    'labor_mnrega_job_cards.csv': ('charthandler.LaborMNREGAJobCards', {
        'Job Cards Issued':           'job_cards_issued',
        'SC':                         'sc',
        'ST':                         'st',
        'Issued for either SC or ST': 'issued_for_sc_or_st',
    }, {'_district_first': True}),

    # ── MNREGA Participation (5 cols) — District first, then Year ─────────────
    'labor_mnrega_participation.csv': ('charthandler.LaborMNREGAParticipation', {
        'Worked':        'worked',
        'Demanded Work': 'demanded_work',
        'Allotted Work': 'allotted_work',
    }, {'_district_first': True}),

    # ── MNREGA Scope (6 cols) — District first, then Year ─────────────────────
    'labor_mnrega_scope.csv': ('charthandler.LaborMNREGAScope', {
        'Applied for a Job Card': 'applied_for_job_card',
        'Worked':                 'worked',
        'Demanded Work':          'demanded_work',
        'Allotted Work':          'allotted_work',
    }, {'_district_first': True}),
}

# Fields stored as strings, not floats
STRING_FIELDS = {
    'rural_urban', 'age_group', 'gender', 'group', 'taluka',
    'select_industry',
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

        self.stdout.write(f'Importing from: {data_dir}\n')

        # Resolve all model classes up front
        model_cache = {}
        for csv_file, (model_path, _, _extra) in CSV_MAP.items():
            app_label, model_name = model_path.rsplit('.', 1)
            model_cache[csv_file] = apps.get_model(app_label, model_name)

        if options['clear']:
            self.stdout.write('Clearing existing labor data...')
            for csv_file, ModelClass in model_cache.items():
                ModelClass.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.\n'))

        total_imported = 0
        for csv_file, (model_path, col_map, extra) in CSV_MAP.items():
            filepath = os.path.join(data_dir, csv_file)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'  [SKIP] {csv_file} (Not found)'))
                continue

            ModelClass = model_cache[csv_file]
            district_first = extra.get('_district_first', False)
            no_year = extra.get('_no_year', False)
            try:
                count = self._import_csv(filepath, ModelClass, col_map, district_first, no_year)
                total_imported += count
                self.stdout.write(
                    self.style.SUCCESS(f'  [OK]   {csv_file} -- {count} records')
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [ERROR] {csv_file}: {e}'))

        self.stdout.write(
            self.style.SUCCESS(f'\nImport complete! Total records: {total_imported}')
        )

    def _import_csv(self, filepath, ModelClass, col_map, district_first=False, no_year=False):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip fully empty rows
                if all(str(v).strip() == '' for v in row.values()):
                    continue

                kwargs = {}

                # District
                district_val = row.get('District', '').strip()
                if not district_val:
                    continue
                kwargs['district'] = district_val

                # Year
                if not no_year:
                    year_raw = row.get('Year', '')
                    year_val = _safe_int(year_raw)
                    if year_val is None:
                        continue
                    kwargs['year'] = year_val

                # All other mapped columns
                for csv_col, model_field in col_map.items():
                    raw = row.get(csv_col, '')
                    if model_field in STRING_FIELDS:
                        kwargs[model_field] = str(raw).strip() if raw else ''
                    else:
                        kwargs[model_field] = _safe_float(raw)

                records.append(ModelClass(**kwargs))

        ModelClass.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
