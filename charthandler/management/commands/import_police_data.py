"""
Management command to import police CSV data into the database.

Usage:
    python manage.py import_police_data [--data-dir PATH] [--clear]

Default data directory: Police/ in the project root.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from charthandler.models.police import (
    PoliceCourtsAppealCases,
    PoliceCourtsFunctioning,
    PoliceCourtsJudgesCases,
    PoliceCourtsOriginalCases,
    PoliceCyberCrimeTypes,
    PoliceCyberFraudTypes,
    PoliceCyberTotals,
    PoliceDSAWomenChildrenTaluka,
    PoliceIPCDocPropertyMarks,
    PoliceIPCHumanBody,
    PoliceIPCMisc,
    PoliceIPCProperty,
    PoliceIPCPublicTranquility,
    PoliceIPCTotal,
    PoliceEmployees,
    PoliceInfrastructure,
    PoliceSLLOffenseTypes,
    PoliceSLLTotal,
    PoliceWomenCrimeTypes,
    PoliceWomenTotal,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_float(value):
    """Safely convert a string to float, returning None for empty/invalid."""
    if value is None or str(value).strip() in ('', 'nan', 'NaN', 'None'):
        return None
    try:
        return float(str(value).strip().replace(',', ''))
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    """Safely convert a string to int via float, returning None for empty/invalid."""
    f = _safe_float(value)
    if f is None:
        return None
    return int(f)


def _str(row, col):
    """Get a stripped string from a CSV row, defaulting to ''."""
    return str(row.get(col, '') or '').strip()


# ---------------------------------------------------------------------------
# All models that will be cleared / imported (in order)
# ---------------------------------------------------------------------------
ALL_MODELS = [
    PoliceCourtsAppealCases,
    PoliceCourtsFunctioning,
    PoliceCourtsJudgesCases,
    PoliceCourtsOriginalCases,
    PoliceCyberCrimeTypes,
    PoliceCyberFraudTypes,
    PoliceCyberTotals,
    PoliceDSAWomenChildrenTaluka,
    PoliceIPCDocPropertyMarks,
    PoliceIPCHumanBody,
    PoliceIPCMisc,
    PoliceIPCProperty,
    PoliceIPCPublicTranquility,
    PoliceIPCTotal,
    PoliceEmployees,
    PoliceInfrastructure,
    PoliceSLLOffenseTypes,
    PoliceSLLTotal,
    PoliceWomenCrimeTypes,
    PoliceWomenTotal,
]


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = 'Import police CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Police'),
            help='Path to the directory containing police CSV files (default: Police/)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing police data before importing',
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']

        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing police data from: {data_dir}\n')

        # --clear: delete all rows from every police model
        if options['clear']:
            self.stdout.write('Clearing existing police data...')
            for ModelClass in ALL_MODELS:
                deleted, _ = ModelClass.objects.all().delete()
                self.stdout.write(f'  Cleared {deleted:>6} rows from {ModelClass.__name__}')
            self.stdout.write(self.style.SUCCESS('All police data cleared.\n'))

        csv_importers = [
            ('Courts_AppealCases.csv', self._import_courts_appeal),
            ('Courts_Functioning.csv', self._import_courts_functioning),
            ('Courts_JudgesCases.csv', self._import_courts_judges),
            ('Courts_OriginalCases.csv', self._import_courts_original),
            ('Cyber_CrimeTypes.csv', self._import_cyber_crime_types),
            ('Cyber_FraudTypes.csv', self._import_cyber_fraud_types),
            ('Cyber_Totals.csv', self._import_cyber_totals),
            ('DSA_WomenChildren_Taluka.csv', self._import_dsa_women_children),
            ('IPC_DocPropertyMarks.csv', self._import_ipc_doc_property),
            ('IPC_HumanBody.csv', self._import_ipc_human_body),
            ('IPC_Misc.csv', self._import_ipc_misc),
            ('IPC_Property.csv', self._import_ipc_property),
            ('IPC_PublicTranquility.csv', self._import_ipc_public_tranq),
            ('IPC_Total.csv', self._import_ipc_total),
            ('Police_Employees.csv', self._import_police_employees),
            ('Police_Infrastructure.csv', self._import_police_infrastructure),
            ('SLL_OffenseTypes.csv', self._import_sll_offense_types),
            ('SLL_Total.csv', self._import_sll_total),
            ('Women_CrimeTypes.csv', self._import_women_crime_types),
            ('Women_Total.csv', self._import_women_total),
        ]

        total_records = 0
        for filename, importer in csv_importers:
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'  [SKIP] {filename} — file not found'))
                continue
            try:
                count = importer(filepath)
                total_records += count
                self.stdout.write(self.style.SUCCESS(f'  [OK]   {filename} — {count} records'))
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f'  [ERROR] {filename}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'\nImport complete! Total records imported: {total_records}'))

    # -------------------------------------------------------------------------
    # Individual importers
    # -------------------------------------------------------------------------

    def _import_courts_appeal(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceCourtsAppealCases(
                    year=year,
                    district=_str(row, 'District'),
                    type_of_court=_str(row, 'Type of Court'),
                    regular=_safe_float(row.get('Regular')),
                    miscellaneous=_safe_float(row.get('Miscellaneous')),
                    all_appeal_cases=_safe_float(row.get('All Appeal Cases')),
                ))
        PoliceCourtsAppealCases.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_courts_functioning(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceCourtsFunctioning(
                    year=year,
                    district=_str(row, 'District'),
                    type_of_court=_str(row, 'Type of Court'),
                    functioning_courts=_safe_float(row.get('Functioning Courts')),
                ))
        PoliceCourtsFunctioning.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_courts_judges(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceCourtsJudgesCases(
                    year=year,
                    district=_str(row, 'District'),
                    type_of_court=_str(row, 'Type of Court'),
                    number_of_functioning_courts=_safe_float(row.get('Number of Functioning courts')),
                    total_cases=_safe_float(row.get('Total Cases')),
                    approved_judge_posts=_safe_float(row.get('Approved Judge Posts')),
                    judge_positions_filled=_safe_float(row.get('Judge Positions Filled')),
                    number_of_regular_original_cases=_safe_float(row.get('Number of Regular Original Cases')),
                    number_of_miscellaneous_original_cases=_safe_float(row.get('Number of Miscellaneous Original Cases')),
                    number_of_regular_appeal_cases=_safe_float(row.get('Number of Regular Appeal Cases')),
                    number_of_miscellaneous_appeal_cases=_safe_float(row.get('Number of Miscellaneous Appeal Cases')),
                ))
        PoliceCourtsJudgesCases.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_courts_original(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceCourtsOriginalCases(
                    year=year,
                    district=_str(row, 'District'),
                    type_of_court=_str(row, 'Type of Court'),
                    regular=_safe_float(row.get('Regular')),
                    miscellaneous=_safe_float(row.get('Miscellaneous')),
                    all_original_cases=_safe_float(row.get('All Original Cases')),
                ))
        PoliceCourtsOriginalCases.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_cyber_crime_types(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceCyberCrimeTypes(
                    year=year,
                    district=_str(row, 'District'),
                    crime=_str(row, 'Crime'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceCyberCrimeTypes.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_cyber_fraud_types(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceCyberFraudTypes(
                    year=year,
                    district=_str(row, 'District'),
                    select_offense=_str(row, 'Select Offense'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceCyberFraudTypes.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_cyber_totals(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceCyberTotals(
                    year=year,
                    district=_str(row, 'District'),
                    offenses_under_it_act=_safe_float(row.get('Offenses under I.T. Act')),
                    fraud=_safe_float(row.get('Fraud')),
                    cyber_crimes=_safe_float(row.get('Cyber Crimes')),
                    offenses_under_ipc_wrt_it_act=_safe_float(row.get('Offenses under IPC wrt IT Act')),
                    offenses_under_sll_wrt_it_act=_safe_float(row.get('Offenses under SLL wrt IT Act')),
                ))
        PoliceCyberTotals.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_women_children(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceDSAWomenChildrenTaluka(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    rape=_safe_float(row.get('Rape')),
                    kidnapping_and_abduction=_safe_float(row.get('Kidnapping and Abduction')),
                    dowry_cases=_safe_float(row.get('Dowry Cases')),
                    sexual_assault=_safe_float(row.get('Sexual Assault')),
                    unethical_business=_safe_float(row.get('Unethical Business')),
                    other_crimes_against_women=_safe_float(row.get('Other Crimes against Women')),
                    murder_womb=_safe_float(row.get('Murder (Womb)')),
                    murder_other=_safe_float(row.get('Murder (other)')),
                    child_rape=_safe_float(row.get('Child Rape')),
                    kidnapping_and_abduction_children=_safe_float(row.get('Kidnapping and Abduction (Children)')),
                    abandonment=_safe_float(row.get('Abandonment')),
                    other_crimes_against_children=_safe_float(row.get('Other Crimes against Children')),
                ))
        PoliceDSAWomenChildrenTaluka.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ipc_doc_property(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceIPCDocPropertyMarks(
                    year=year,
                    district=_str(row, 'District'),
                    select_offense=_str(row, 'Select Offense'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceIPCDocPropertyMarks.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ipc_human_body(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceIPCHumanBody(
                    year=year,
                    district=_str(row, 'District'),
                    crime=_str(row, 'Crime'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceIPCHumanBody.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ipc_misc(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceIPCMisc(
                    year=year,
                    district=_str(row, 'District'),
                    select_offense=_str(row, 'Select Offense'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceIPCMisc.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ipc_property(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceIPCProperty(
                    year=year,
                    district=_str(row, 'District'),
                    crime=_str(row, 'Crime'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceIPCProperty.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ipc_public_tranq(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceIPCPublicTranquility(
                    year=year,
                    district=_str(row, 'District'),
                    crime=_str(row, 'Crime'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceIPCPublicTranquility.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ipc_total(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceIPCTotal(
                    year=year,
                    district=_str(row, 'District'),
                    cognizable_ipc_crimes=_safe_float(row.get('Cognizable IPC crimes')),
                ))
        PoliceIPCTotal.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_police_employees(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceEmployees(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    establishment=_str(row, 'Establishment'),
                    number_of_officers_employees=_safe_float(row.get('Number of Officers/Employees')),
                ))
        PoliceEmployees.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_police_infrastructure(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceInfrastructure(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    select_type_of_police_establishment=_str(row, 'Select Type of Police Establishment'),
                    number=_safe_float(row.get('Number')),
                ))
        PoliceInfrastructure.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_sll_offense_types(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceSLLOffenseTypes(
                    year=year,
                    district=_str(row, 'District'),
                    select_offense_under=_str(row, 'Select Offense Under'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceSLLOffenseTypes.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_sll_total(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceSLLTotal(
                    year=year,
                    district=_str(row, 'District'),
                    cognizable_sll_crimes=_safe_float(row.get('Cognizable SLL Crimes')),
                ))
        PoliceSLLTotal.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_women_crime_types(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceWomenCrimeTypes(
                    year=year,
                    district=_str(row, 'District'),
                    crime=_str(row, 'Crime'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceWomenCrimeTypes.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_women_total(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(PoliceWomenTotal(
                    year=year,
                    district=_str(row, 'District'),
                    cases=_safe_float(row.get('Cases')),
                ))
        PoliceWomenTotal.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
