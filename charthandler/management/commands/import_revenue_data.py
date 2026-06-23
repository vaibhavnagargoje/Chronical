"""
Management command to import revenue CSV data into the database.

Usage:
    python manage.py import_revenue_data [--data-dir PATH]

Default data directory: Revenue/ in the project root.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from charthandler.models.revenue import (
    RevenueDSABanking,
    RevenueDSABankingN,
    RevenueDSADepositsN,
    RevenueDSAGramPanchayat,
    RevenueDSAGramPanchayatN,
    RevenueDSAGST,
    RevenueDSAJillaParishadExp,
    RevenueDSAJillaParishadInc,
    RevenueDSAJillaParishadN,
    RevenueDSALandRevenue,
    RevenueDSALandRevenueN,
    RevenueDSALoansN,
    RevenueDSAMunCorpN,
    RevenueDSAMunicipalCorpExp,
    RevenueDSAMunicipalCorpInc,
    RevenueDSAMunicipalCounExp,
    RevenueDSAMunicipalCounInc,
    RevenueDSAMunicipalCounN,
    RevenueDSANagarPanchayatExp,
    RevenueDSANagarPanchayatInc,
    RevenueDSANagarPanchayatN,
    RevenueDSATaxRevenue,
    RevenueDSATaxRevenueN,
    RevenueGDDPGDVA,
    RevenueGDDPGDVAN,
    RevenueNDDPNDVA,
    RevenueNDDPNDVAN,
)

def _safe_float(value):
    if value is None or str(value).strip() == '':
        return None
    try:
        return float(str(value).strip().replace(',', ''))
    except (ValueError, TypeError):
        return None

def _safe_int(value):
    f = _safe_float(value)
    if f is None:
        return None
    return int(f)

class Command(BaseCommand):
    help = 'Import revenue CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Revenue'),
            help='Path to the directory containing revenue CSV files'
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
            self.stdout.write('Clearing existing revenue data...')
            RevenueDSABanking.objects.all().delete()
            RevenueDSABankingN.objects.all().delete()
            RevenueDSADepositsN.objects.all().delete()
            RevenueDSAGramPanchayat.objects.all().delete()
            RevenueDSAGramPanchayatN.objects.all().delete()
            RevenueDSAGST.objects.all().delete()
            RevenueDSAJillaParishadExp.objects.all().delete()
            RevenueDSAJillaParishadInc.objects.all().delete()
            RevenueDSAJillaParishadN.objects.all().delete()
            RevenueDSALandRevenue.objects.all().delete()
            RevenueDSALandRevenueN.objects.all().delete()
            RevenueDSALoansN.objects.all().delete()
            RevenueDSAMunCorpN.objects.all().delete()
            RevenueDSAMunicipalCorpExp.objects.all().delete()
            RevenueDSAMunicipalCorpInc.objects.all().delete()
            RevenueDSAMunicipalCounExp.objects.all().delete()
            RevenueDSAMunicipalCounInc.objects.all().delete()
            RevenueDSAMunicipalCounN.objects.all().delete()
            RevenueDSANagarPanchayatExp.objects.all().delete()
            RevenueDSANagarPanchayatInc.objects.all().delete()
            RevenueDSANagarPanchayatN.objects.all().delete()
            RevenueDSATaxRevenue.objects.all().delete()
            RevenueDSATaxRevenueN.objects.all().delete()
            RevenueGDDPGDVA.objects.all().delete()
            RevenueGDDPGDVAN.objects.all().delete()
            RevenueNDDPNDVA.objects.all().delete()
            RevenueNDDPNDVAN.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        csv_files = {
            'DSA_Banking.csv': self._import_dsa_banking,
            'DSA_Banking_N.csv': self._import_dsa_banking_n,
            'DSA_Deposits_N.csv': self._import_dsa_deposits_n,
            'DSA_GramPanchayat.csv': self._import_dsa_grampanchayat,
            'DSA_GramPanchayat_N.csv': self._import_dsa_grampanchayat_n,
            'DSA_GST.csv': self._import_dsa_gst,
            'DSA_JillaParishad_Exp.csv': self._import_dsa_jillaparishad_exp,
            'DSA_JillaParishad_Inc.csv': self._import_dsa_jillaparishad_inc,
            'DSA_JillaParishad_N.csv': self._import_dsa_jillaparishad_n,
            'DSA_LandRevenue.csv': self._import_dsa_landrevenue,
            'DSA_LandRevenue_N.csv': self._import_dsa_landrevenue_n,
            'DSA_Loans_N.csv': self._import_dsa_loans_n,
            'DSA_MunCorp_N.csv': self._import_dsa_muncorp_n,
            'DSA_MunicipalCorp_Exp.csv': self._import_dsa_municipalcorp_exp,
            'DSA_MunicipalCorp_Inc.csv': self._import_dsa_municipalcorp_inc,
            'DSA_MunicipalCoun_Exp.csv': self._import_dsa_municipalcoun_exp,
            'DSA_MunicipalCoun_Inc.csv': self._import_dsa_municipalcoun_inc,
            'DSA_MunicipalCoun_N.csv': self._import_dsa_municipalcoun_n,
            'DSA_NagarPanchayat_Exp.csv': self._import_dsa_nagarpanchayat_exp,
            'DSA_NagarPanchayat_Inc.csv': self._import_dsa_nagarpanchayat_inc,
            'DSA_NagarPanchayat_N.csv': self._import_dsa_nagarpanchayat_n,
            'DSA_TaxRevenue.csv': self._import_dsa_taxrevenue,
            'DSA_TaxRevenue_N.csv': self._import_dsa_taxrevenue_n,
            'GDDP_GDVA.csv': self._import_gddp_gdva,
            'GDDP_GDVA_N.csv': self._import_gddp_gdva_n,
            'NDDP_NDVA.csv': self._import_nddp_ndva,
            'NDDP_NDVA_N.csv': self._import_nddp_ndva_n,
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

    def _import_dsa_banking(self, filepath):
        """Import DSA_Banking.csv → RevenueDSABanking"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSABanking(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    taluka=row.get('Taluka', '').strip() if row.get('Taluka') else None,
                    towns_and_cities_where_banks_have_offices=_safe_float(row.get('Towns and cities where banks have offices')),
                    classified_banks=_safe_float(row.get('Classified Banks')),
                    branch_offices_of_classified_banks=_safe_float(row.get('Branch Offices of Classified Banks')),
                    deposits=_safe_float(row.get('Deposits')),
                    agriculture_loans=_safe_float(row.get('Agriculture Loans')),
                    non_agriculture_loans=_safe_float(row.get('Non-Agriculture Loans')),
                    total_loans=_safe_float(row.get('Total Loans')),
                ))
        RevenueDSABanking.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_banking_n(self, filepath):
        """Import DSA_Banking_N.csv → RevenueDSABankingN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSABankingN(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    taluka=row.get('Taluka', '').strip() if row.get('Taluka') else None,
                    towns_and_cities_where_banks_have_offices=_safe_float(row.get('Towns and cities where banks have offices')),
                    classified_banks=_safe_float(row.get('Classified Banks')),
                    branch_offices_of_classified_banks=_safe_float(row.get('Branch Offices of Classified Banks')),
                ))
        RevenueDSABankingN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_deposits_n(self, filepath):
        """Import DSA_Deposits_N.csv → RevenueDSADepositsN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSADepositsN(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    taluka_old=row.get('Taluka Old', '').strip() if row.get('Taluka Old') else None,
                    taluka=row.get('Taluka', '').strip() if row.get('Taluka') else None,
                    deposits=_safe_float(row.get('Deposits')),
                ))
        RevenueDSADepositsN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_grampanchayat(self, filepath):
        """Import DSA_GramPanchayat.csv → RevenueDSAGramPanchayat"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAGramPanchayat(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    land_and_property_taxes=_safe_float(row.get('Land and Property taxes')),
                    other_taxes_and_charges=_safe_float(row.get('Other taxes and charges')),
                    tax=_safe_float(row.get('Tax')),
                    statutory_grants=_safe_float(row.get('Statutory Grants')),
                    contribution_donations_and_other_subsidies=_safe_float(row.get('Contribution, donations and other subsidies')),
                    grants=_safe_float(row.get('Grants')),
                    other_sources=_safe_float(row.get('Other Sources')),
                    revenue=_safe_float(row.get('Revenue')),
                    administration=_safe_float(row.get('Administration\n')),
                    public_health=_safe_float(row.get('Public Health\n')),
                    public_works=_safe_float(row.get('Public Works\n')),
                    public_lighting=_safe_float(row.get('Public Lighting\n')),
                    education=_safe_float(row.get('Education\n')),
                    public_welfare=_safe_float(row.get('Public Welfare\n')),
                    other_expenses=_safe_float(row.get('Other Expenses\n')),
                    developmental=_safe_float(row.get('Developmental')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    total_deposit=_safe_float(row.get('Total Deposit')),
                ))
        RevenueDSAGramPanchayat.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_grampanchayat_n(self, filepath):
        """Import DSA_GramPanchayat_N.csv → RevenueDSAGramPanchayatN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAGramPanchayatN(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    land_and_property_taxes=_safe_float(row.get('Land and Property taxes')),
                    other_taxes_and_charges=_safe_float(row.get('Other taxes and charges')),
                    tax=_safe_float(row.get('Tax')),
                    government_grants=_safe_float(row.get('Government Grants')),
                    contribution_donations_and_other_grants=_safe_float(row.get('Contribution, donations and other grants')),
                    grants=_safe_float(row.get('Grants')),
                    other_sources=_safe_float(row.get('Other Sources')),
                    revenue=_safe_float(row.get('Revenue')),
                    administration=_safe_float(row.get('Administration\n')),
                    health_and_hygiene=_safe_float(row.get('Health and Hygiene\n')),
                    public_works=_safe_float(row.get('Public Works\n')),
                    public_lighting=_safe_float(row.get('Public Lighting\n')),
                    education=_safe_float(row.get('Education\n')),
                    public_welfare=_safe_float(row.get('Public Welfare\n')),
                    other_expenses=_safe_float(row.get('Other Expenses\n')),
                    developmental=_safe_float(row.get('Developmental')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    total_deposit=_safe_float(row.get('Total Deposit')),
                ))
        RevenueDSAGramPanchayatN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_gst(self, filepath):
        """Import DSA_GST.csv → RevenueDSAGST"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAGST(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    vat=_safe_float(row.get('VAT')),
                    central_sales_tax=_safe_float(row.get('Central Sales Tax')),
                    business_tax=_safe_float(row.get('Business Tax')),
                    sugarcane_purchase_tax=_safe_float(row.get('Sugarcane purchase tax')),
                    entry_tax=_safe_float(row.get('Entry Tax')),
                    luxury_tax=_safe_float(row.get('Luxury Tax')),
                    gst=_safe_float(row.get('GST')),
                    total=_safe_float(row.get('Total')),
                ))
        RevenueDSAGST.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_jillaparishad_exp(self, filepath):
        """Import DSA_JillaParishad_Exp.csv → RevenueDSAJillaParishadExp"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAJillaParishadExp(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    general_administration=_safe_float(row.get('General Administration')),
                    education=_safe_float(row.get('Education')),
                    public_works=_safe_float(row.get('Public Works')),
                    irrigation=_safe_float(row.get('Irrigation')),
                    agriculture=_safe_float(row.get('Agriculture')),
                    animal_husbandary=_safe_float(row.get('Animal Husbandary')),
                    forests=_safe_float(row.get('Forests')),
                    public_health=_safe_float(row.get('Public Health')),
                    social_welfare=_safe_float(row.get('Social Welfare')),
                    other_expenses=_safe_float(row.get('Other Expenses')),
                    revenue_account=_safe_float(row.get('Revenue Account')),
                    capital_account=_safe_float(row.get('Capital Account')),
                    total_expenditure=_safe_float(row.get('Total Expenditure')),
                ))
        RevenueDSAJillaParishadExp.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_jillaparishad_inc(self, filepath):
        """Import DSA_JillaParishad_Inc.csv → RevenueDSAJillaParishadInc"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAJillaParishadInc(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    opening_balance=_safe_float(row.get('Opening Balance')),
                    self_generated=_safe_float(row.get('Self-Generated')),
                    purposive_grants=_safe_float(row.get('Purposive Grants')),
                    establishment_grants=_safe_float(row.get('Establishment Grants')),
                    grants_for_plan_schemes=_safe_float(row.get('Grants for Plan Schemes')),
                    other_statutory_grants=_safe_float(row.get('Other Statutory Grants')),
                    statutory_grants=_safe_float(row.get('Statutory Grants')),
                    for_agency_schemes=_safe_float(row.get('For Agency Schemes')),
                    government_subsidies=_safe_float(row.get('Government Subsidies')),
                    other_income=_safe_float(row.get('Other Income')),
                    revenue_income=_safe_float(row.get('Revenue Income')),
                    capital_income=_safe_float(row.get('Capital Income')),
                    all_receipts=_safe_float(row.get('All Receipts')),
                    revenue=_safe_float(row.get('Revenue')),
                    general_administration=_safe_float(row.get('General Administration')),
                    education=_safe_float(row.get('Education')),
                    public_works=_safe_float(row.get('Public Works')),
                    irrigation=_safe_float(row.get('Irrigation')),
                    agriculture=_safe_float(row.get('Agriculture')),
                    animal_husbandary=_safe_float(row.get('Animal Husbandary')),
                    forests=_safe_float(row.get('Forests')),
                    public_health=_safe_float(row.get('Public Health')),
                    social_welfare=_safe_float(row.get('Social Welfare')),
                    other_expenses=_safe_float(row.get('Other Expenses')),
                    revenue_expenditure=_safe_float(row.get('Revenue Expenditure')),
                    capital_expenditure=_safe_float(row.get('Capital Expenditure')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    economic_services=_safe_float(row.get('Economic Services')),
                    social_services=_safe_float(row.get('Social Services')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                ))
        RevenueDSAJillaParishadInc.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_jillaparishad_n(self, filepath):
        """Import DSA_JillaParishad_N.csv → RevenueDSAJillaParishadN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAJillaParishadN(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    opening_balance=_safe_float(row.get('Opening Balance')),
                    self_generated=_safe_float(row.get('Self-Generated')),
                    purposive_grants=_safe_float(row.get('Purposive Grants')),
                    establishment_grants=_safe_float(row.get('Establishment Grants')),
                    grants_for_plan_schemes=_safe_float(row.get('Grants for Plan Schemes')),
                    other_statutory_grants=_safe_float(row.get('Other Statutory Grants')),
                    statutory_grants=_safe_float(row.get('Statutory Grants')),
                    for_agency_schemes=_safe_float(row.get('For Agency Schemes')),
                    total_grants=_safe_float(row.get('Total Grants')),
                    other_income=_safe_float(row.get('Other Income')),
                    revenue_income=_safe_float(row.get('Revenue Income')),
                    capital_income=_safe_float(row.get('Capital Income')),
                    all_receipts=_safe_float(row.get('All Receipts')),
                    revenue=_safe_float(row.get('Revenue')),
                    general_administration=_safe_float(row.get('General Administration')),
                    education=_safe_float(row.get('Education')),
                    public_works=_safe_float(row.get('Public Works')),
                    irrigation=_safe_float(row.get('Irrigation')),
                    agriculture=_safe_float(row.get('Agriculture')),
                    animal_husbandary=_safe_float(row.get('Animal Husbandary')),
                    forests=_safe_float(row.get('Forests')),
                    public_health=_safe_float(row.get('Public Health')),
                    social_welfare=_safe_float(row.get('Social Welfare')),
                    other_expenses=_safe_float(row.get('Other Expenses')),
                    revenue_expenditure=_safe_float(row.get('Revenue Expenditure')),
                    capital_expenditure=_safe_float(row.get('Capital Expenditure')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    economic_services=_safe_float(row.get('Economic Services')),
                    social_services=_safe_float(row.get('Social Services')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                ))
        RevenueDSAJillaParishadN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_landrevenue(self, filepath):
        """Import DSA_LandRevenue.csv → RevenueDSALandRevenue"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSALandRevenue(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    taluka=row.get('Taluka', '').strip() if row.get('Taluka') else None,
                    aggregate_current_demand=_safe_float(row.get('Aggregate Current Demand')),
                    arrears=_safe_float(row.get('Arrears')),
                    aggregate_demand=_safe_float(row.get('Aggregate Demand')),
                    discount=_safe_float(row.get('Discount')),
                    amount_of_suspended_recovery=_safe_float(row.get('Amount of suspended recovery')),
                    amount_eligible_for_recovery=_safe_float(row.get('Amount Eligible for Recovery')),
                    value_recovery=_safe_float(row.get('Value Recovery')),
                    number_of_account_holders=_safe_float(row.get('Number of Account Holders')),
                ))
        RevenueDSALandRevenue.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_landrevenue_n(self, filepath):
        """Import DSA_LandRevenue_N.csv → RevenueDSALandRevenueN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSALandRevenueN(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    taluka=row.get('Taluka', '').strip() if row.get('Taluka') else None,
                    aggregate_current_demand=_safe_float(row.get('Aggregate Current Demand')),
                    arrears=_safe_float(row.get('Arrears')),
                    aggregate_demand=_safe_float(row.get('Aggregate Demand')),
                    discount=_safe_float(row.get('Discount')),
                    amount_of_suspended_recovery=_safe_float(row.get('Amount of suspended recovery')),
                    amount_eligible_for_recovery=_safe_float(row.get('Amount Eligible for Recovery')),
                    value_recovery=_safe_float(row.get('Value Recovery')),
                    number_of_account_holders=_safe_float(row.get('Number of Account Holders')),
                ))
        RevenueDSALandRevenueN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_loans_n(self, filepath):
        """Import DSA_Loans_N.csv → RevenueDSALoansN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSALoansN(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    taluka_old=row.get('Taluka Old', '').strip() if row.get('Taluka Old') else None,
                    taluka=row.get('Taluka', '').strip() if row.get('Taluka') else None,
                    agriculture_loans=_safe_float(row.get('Agriculture Loans')),
                    non_agriculture_loans=_safe_float(row.get('Non-Agriculture Loans')),
                    total_loans=_safe_float(row.get('Total Loans')),
                ))
        RevenueDSALoansN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_muncorp_n(self, filepath):
        """Import DSA_MunCorp_N.csv → RevenueDSAMunCorpN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAMunCorpN(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    receipts_and_loans=_safe_float(row.get('Receipts and Loans\n')),
                    from_commercial_activities=_safe_float(row.get('From Commercial Activities\n')),
                    government_subsidy=_safe_float(row.get('Government Subsidy')),
                    other_sources=_safe_float(row.get('Other Sources\n')),
                    rents_and_taxes=_safe_float(row.get('Rents and Taxes')),
                    revenue=_safe_float(row.get('Revenue\n')),
                    administration_establishment=_safe_float(row.get('Administration (Establishment)')),
                    administration_others=_safe_float(row.get('Administration (Others)')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_components=_safe_float(row.get('Expenditure on Weak Components')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    social_services=_safe_float(row.get('Social Services')),
                    economic_services=_safe_float(row.get('Economic Services')),
                    developmental=_safe_float(row.get('Developmental')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                ))
        RevenueDSAMunCorpN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_municipalcorp_exp(self, filepath):
        """Import DSA_MunicipalCorp_Exp.csv → RevenueDSAMunicipalCorpExp"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAMunicipalCorpExp(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    administration_establishment=_safe_float(row.get('Administration-Establishment')),
                    administration_others=_safe_float(row.get('Administration-Others')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_components=_safe_float(row.get('Expenditure on Weak Components')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    total_expenditure=_safe_float(row.get('Total Expenditure')),
                ))
        RevenueDSAMunicipalCorpExp.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_municipalcorp_inc(self, filepath):
        """Import DSA_MunicipalCorp_Inc.csv → RevenueDSAMunicipalCorpInc"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAMunicipalCorpInc(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    receipts_and_loans=_safe_float(row.get('Receipts and Loans\n')),
                    from_commercial_activities=_safe_float(row.get('From Commercial Activities\n')),
                    government_grants=_safe_float(row.get('Government Grants')),
                    other_sources=_safe_float(row.get('Other Sources\n')),
                    rents_and_taxes=_safe_float(row.get('Rents and Taxes')),
                    revenue=_safe_float(row.get('Revenue\n')),
                    administration_establishment=_safe_float(row.get('Administration (Establishment)')),
                    administration_others=_safe_float(row.get('Administration (Others)')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_components=_safe_float(row.get('Expenditure on Weak Components')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    social_services=_safe_float(row.get('Social Services')),
                    economic_services=_safe_float(row.get('Economic Services')),
                    developmental=_safe_float(row.get('Developmental')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                ))
        RevenueDSAMunicipalCorpInc.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_municipalcoun_exp(self, filepath):
        """Import DSA_MunicipalCoun_Exp.csv → RevenueDSAMunicipalCounExp"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAMunicipalCounExp(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    administration_establishment=_safe_float(row.get('Administration (Establishment)')),
                    administration_others=_safe_float(row.get('Administration (Others)')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_sectors=_safe_float(row.get('Expenditure on Weak Sectors')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    total_expenditure=_safe_float(row.get('Total Expenditure')),
                ))
        RevenueDSAMunicipalCounExp.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_municipalcoun_inc(self, filepath):
        """Import DSA_MunicipalCoun_Inc.csv → RevenueDSAMunicipalCounInc"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAMunicipalCounInc(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    receipts_and_loans=_safe_float(row.get('Receipts and Loans\n')),
                    from_commercial_activities=_safe_float(row.get('From Commercial Activities\n')),
                    government_grants=_safe_float(row.get('Government Grants')),
                    other_sources=_safe_float(row.get('Other Sources\n')),
                    rents_and_taxes=_safe_float(row.get('Rents and Taxes')),
                    revenue=_safe_float(row.get('Revenue\n')),
                    administration_establishment=_safe_float(row.get('Administration (Establishment)')),
                    administration_others=_safe_float(row.get('Administration (Others)')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_sectors=_safe_float(row.get('Expenditure on Weak Sectors')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    social_services=_safe_float(row.get('Social Services')),
                    economic_services=_safe_float(row.get('Economic Services')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                ))
        RevenueDSAMunicipalCounInc.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_municipalcoun_n(self, filepath):
        """Import DSA_MunicipalCoun_N.csv → RevenueDSAMunicipalCounN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSAMunicipalCounN(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    receipts_and_loans=_safe_float(row.get('Receipts and Loans\n')),
                    from_commercial_activities=_safe_float(row.get('From Commercial Activities\n')),
                    government_subsidies=_safe_float(row.get('Government Subsidies')),
                    other_sources=_safe_float(row.get('Other Sources\n')),
                    rents_and_taxes=_safe_float(row.get('Rents and Taxes')),
                    revenue=_safe_float(row.get('Revenue\n')),
                    administration_establishment=_safe_float(row.get('Administration (Establishment)')),
                    administration_others=_safe_float(row.get('Administration (Others)')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_sectors=_safe_float(row.get('Expenditure on Weak Sectors')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    social_services=_safe_float(row.get('Social Services')),
                    economic_services=_safe_float(row.get('Economic Services')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                ))
        RevenueDSAMunicipalCounN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_nagarpanchayat_exp(self, filepath):
        """Import DSA_NagarPanchayat_Exp.csv → RevenueDSANagarPanchayatExp"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSANagarPanchayatExp(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    administration_establishment=_safe_float(row.get('Administration-Establishment')),
                    administration_others=_safe_float(row.get('Administration-Others')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_components=_safe_float(row.get('Expenditure on Weak Components')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    total_expenditure=_safe_float(row.get('Total Expenditure')),
                ))
        RevenueDSANagarPanchayatExp.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_nagarpanchayat_inc(self, filepath):
        """Import DSA_NagarPanchayat_Inc.csv → RevenueDSANagarPanchayatInc"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSANagarPanchayatInc(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    receipts_and_loans=_safe_float(row.get('Receipts and Loans')),
                    from_commercial_activities=_safe_float(row.get('From Commercial Activities\n')),
                    government_grants=_safe_float(row.get('Government Grants')),
                    other_sources=_safe_float(row.get('Other Sources')),
                    rents_and_taxes=_safe_float(row.get('Rents and Taxes')),
                    revenue=_safe_float(row.get('Revenue')),
                    administration_establishment=_safe_float(row.get('Administration (Establishment)')),
                    administration_others=_safe_float(row.get('Administration (Others)')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_components=_safe_float(row.get('Expenditure on Weak Components')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    social_services=_safe_float(row.get('Social Services')),
                    economic_services=_safe_float(row.get('Economic Services')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                ))
        RevenueDSANagarPanchayatInc.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_nagarpanchayat_n(self, filepath):
        """Import DSA_NagarPanchayat_N.csv → RevenueDSANagarPanchayatN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSANagarPanchayatN(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    receipts_and_loans=_safe_float(row.get('Receipts and Loans')),
                    from_commercial_activities=_safe_float(row.get('From Commercial Activities\n')),
                    government_subsidies=_safe_float(row.get('Government Subsidies')),
                    other_sources=_safe_float(row.get('Other Sources')),
                    rents_and_taxes=_safe_float(row.get('Rents and Taxes')),
                    revenue=_safe_float(row.get('Revenue')),
                    administration_establishment=_safe_float(row.get('Administration (Establishment)')),
                    administration_others=_safe_float(row.get('Administration (Others)')),
                    construction=_safe_float(row.get('Construction')),
                    drainage_and_sewage=_safe_float(row.get('Drainage and Sewage')),
                    education=_safe_float(row.get('Education')),
                    expenditure_on_weak_components=_safe_float(row.get('Expenditure on Weak Components')),
                    others=_safe_float(row.get('Others')),
                    public_health=_safe_float(row.get('Public Health')),
                    public_lighting=_safe_float(row.get('Public Lighting')),
                    public_security=_safe_float(row.get('Public Security')),
                    special_expenses_and_loans=_safe_float(row.get('Special Expenses and Loans')),
                    tax_recovery=_safe_float(row.get('Tax Recovery')),
                    transportation=_safe_float(row.get('Transportation')),
                    water_supply=_safe_float(row.get('Water Supply')),
                    expenditure=_safe_float(row.get('Expenditure')),
                    social_services=_safe_float(row.get('Social Services')),
                    economic_services=_safe_float(row.get('Economic Services')),
                    non_developmental=_safe_float(row.get('Non-Developmental')),
                ))
        RevenueDSANagarPanchayatN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_taxrevenue(self, filepath):
        """Import DSA_TaxRevenue.csv → RevenueDSATaxRevenue"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSATaxRevenue(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    value_added_tax_vat=_safe_float(row.get('Value Added Tax (VAT)')),
                    stamp_and_registration_fee=_safe_float(row.get('Stamp and Registration fee')),
                    state_excise_duty=_safe_float(row.get('State Excise Duty')),
                    electricity_charges=_safe_float(row.get('Electricity Charges')),
                    entertainment_tax=_safe_float(row.get('Entertainment Tax')),
                    vehicles_tax=_safe_float(row.get('Vehicles Tax')),
                    tax_on_goods_and_cargo=_safe_float(row.get('Tax on goods and cargo')),
                    land_tax=_safe_float(row.get('Land Tax')),
                    other_revenue=_safe_float(row.get('Other Revenue')),
                    total_tax_revenue=_safe_float(row.get('Total Tax Revenue')),
                ))
        RevenueDSATaxRevenue.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_taxrevenue_n(self, filepath):
        """Import DSA_TaxRevenue_N.csv → RevenueDSATaxRevenueN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueDSATaxRevenueN(
                    district=row.get('District', '').strip() if row.get('District') else None,
                    year=year,
                    value_added_tax_vat=_safe_float(row.get('Value Added Tax (VAT)')),
                    stamp_and_registration_fee=_safe_float(row.get('Stamp and Registration fee')),
                    state_excise_duty=_safe_float(row.get('State Excise Duty')),
                    electricity_charges=_safe_float(row.get('Electricity Charges')),
                    entertainment_tax=_safe_float(row.get('Entertainment Tax')),
                    vehicles_tax=_safe_float(row.get('Vehicles Tax')),
                    tax_on_goods_and_cargo=_safe_float(row.get('Tax on goods and cargo')),
                    land_tax=_safe_float(row.get('Land Tax')),
                    other_revenue=_safe_float(row.get('Other Revenue')),
                    total_tax_revenue=_safe_float(row.get('Total Tax Revenue')),
                ))
        RevenueDSATaxRevenueN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_gddp_gdva(self, filepath):
        """Import GDDP_GDVA.csv → RevenueGDDPGDVA"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueGDDPGDVA(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    crops=_safe_float(row.get('Crops')),
                    livestock=_safe_float(row.get('Livestock')),
                    forestry_and_logging=_safe_float(row.get('Forestry and Logging')),
                    fishing_and_aquaculture=_safe_float(row.get('Fishing and aquaculture')),
                    agriculture_allied_activities=_safe_float(row.get('Agriculture & Allied Activities')),
                    mining_quarrying=_safe_float(row.get('Mining & Quarrying')),
                    primary_sector=_safe_float(row.get('Primary Sector')),
                    manufacturing=_safe_float(row.get('Manufacturing')),
                    electricity_gas_water_supply_other_utility_services=_safe_float(row.get('Electricity, Gas, Water Supply  & Other Utility\nServices')),
                    construction=_safe_float(row.get('Construction')),
                    secondary_sector=_safe_float(row.get('Secondary Sector')),
                    industry=_safe_float(row.get('Industry')),
                    trade_repair_hotels_restaurants=_safe_float(row.get('Trade, Repair, Hotels &\nRestaurants')),
                    railways=_safe_float(row.get('Railways')),
                    transport_by_means_other_than_railways=_safe_float(row.get('Transport by means other than\nRailways')),
                    storage=_safe_float(row.get('Storage')),
                    comm_and_services_related_to_broad=_safe_float(row.get('Comm. and services related to\nBroad.')),
                    financial_services=_safe_float(row.get('Financial Services')),
                    r_estate_o_dwellings_professional_services=_safe_float(row.get('R. Estate, O. Dwellings & Professional\nServices')),
                    public_administration_defence=_safe_float(row.get('Public Administration\nDefence')),
                    other_services=_safe_float(row.get('Other Services')),
                    services_tertiary_sector=_safe_float(row.get('Services/ Tertiary Sector')),
                    gdva=_safe_float(row.get('GDVA')),
                    taxes_on_products=_safe_float(row.get('Taxes on products')),
                    less_subsidies_on_products=_safe_float(row.get('Less subsidies on\nproducts')),
                    gddp=_safe_float(row.get('GDDP')),
                    population_000=_safe_float(row.get("Population ('000)")),
                    per_capita_district_domestic_product=_safe_float(row.get('Per capita District Domestic Product')),
                ))
        RevenueGDDPGDVA.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_gddp_gdva_n(self, filepath):
        """Import GDDP_GDVA_N.csv → RevenueGDDPGDVAN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueGDDPGDVAN(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    crops=_safe_float(row.get('Crops')),
                    livestock=_safe_float(row.get('Livestock')),
                    forestry_and_logging=_safe_float(row.get('Forestry and Logging')),
                    fishing_and_aquaculture=_safe_float(row.get('Fishing and aquaculture')),
                    agriculture_allied_activities=_safe_float(row.get('Agriculture & Allied Activities')),
                    mining_quarrying=_safe_float(row.get('Mining & Quarrying')),
                    primary_sector=_safe_float(row.get('Primary Sector')),
                    manufacturing=_safe_float(row.get('Manufacturing')),
                    electricity_gas_water_supply_other_utility_services=_safe_float(row.get('Electricity, Gas, Water Supply  & Other Utility\nServices')),
                    construction=_safe_float(row.get('Construction')),
                    secondary_sector=_safe_float(row.get('Secondary Sector')),
                    industry=_safe_float(row.get('Industry')),
                    trade_repair_and_hospitality=_safe_float(row.get('Trade, Repair, and Hospitality')),
                    railways=_safe_float(row.get('Railways')),
                    transport_other_than_railways=_safe_float(row.get('Transport (Other than Railways)')),
                    storage=_safe_float(row.get('Storage')),
                    communication_and_broadcast_services=_safe_float(row.get('Communication and Broadcast Services')),
                    financial_services=_safe_float(row.get('Financial Services')),
                    real_estate_other_dwellings_and_professional_services=_safe_float(row.get('Real Estate, Other Dwellings, and Professional Services')),
                    public_administration_and_defence=_safe_float(row.get('Public Administration and Defence')),
                    other_services=_safe_float(row.get('Other Services')),
                    services_tertiary_sector=_safe_float(row.get('Services/ Tertiary Sector')),
                    gdva=_safe_float(row.get('GDVA')),
                    taxes_on_products=_safe_float(row.get('Taxes on products')),
                    less_subsidies_on_products=_safe_float(row.get('Less subsidies on\nproducts')),
                    gddp=_safe_float(row.get('GDDP')),
                    population_000=_safe_float(row.get("Population ('000)")),
                    per_capita_district_domestic_product=_safe_float(row.get('Per capita District Domestic Product')),
                ))
        RevenueGDDPGDVAN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_nddp_ndva(self, filepath):
        """Import NDDP_NDVA.csv → RevenueNDDPNDVA"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueNDDPNDVA(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    crops=_safe_float(row.get('Crops')),
                    livestock=_safe_float(row.get('Livestock')),
                    forestry_and_logging=_safe_float(row.get('Forestry and Logging')),
                    fishing_and_aquaculture=_safe_float(row.get('Fishing and aquaculture')),
                    agriculture_allied_activities=_safe_float(row.get('Agriculture & Allied Activities')),
                    minign_quarrying=_safe_float(row.get('Minign & Quarrying')),
                    primary_sector=_safe_float(row.get('Primary Sector')),
                    manufacturing=_safe_float(row.get('Manufacturing')),
                    electricity_gas_water_supply_other_utility_services=_safe_float(row.get('Electricity, Gas, Water Supply  & Other Utility\nServices')),
                    construction=_safe_float(row.get('Construction')),
                    secondary_sector=_safe_float(row.get('Secondary Sector')),
                    industry=_safe_float(row.get('Industry')),
                    trade_repair_hotels_restaurants=_safe_float(row.get('Trade, Repair, Hotels &\nRestaurants')),
                    railways=_safe_float(row.get('Railways')),
                    transport_by_means_other_than_railways=_safe_float(row.get('Transport by means other than\nRailways')),
                    storage=_safe_float(row.get('Storage')),
                    comm_and_services_related_to_broad=_safe_float(row.get('Comm. and services related to\nBroad.')),
                    financial_services=_safe_float(row.get('Financial Services')),
                    r_estate_o_dwellings_professional_services=_safe_float(row.get('R. Estate, O. Dwellings & Professional\nServices')),
                    public_admini_stration_defence=_safe_float(row.get('Public Admini- stration &\nDefence')),
                    other_services=_safe_float(row.get('Other Services')),
                    services_tertiary_sector=_safe_float(row.get('Services/ Tertiary Sector')),
                    ndva=_safe_float(row.get('NDVA')),
                    taxes_on_products=_safe_float(row.get('Taxes on products')),
                    less_subsidies_on_products=_safe_float(row.get('Less subsidies on\nproducts')),
                    nddp=_safe_float(row.get('NDDP')),
                    popula_tion_000=_safe_float(row.get("Popula- tion ('000)")),
                    per_capita_district_domestic_product=_safe_float(row.get('Per capita District Domestic\nProduct  (  )')),
                ))
        RevenueNDDPNDVA.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_nddp_ndva_n(self, filepath):
        """Import NDDP_NDVA_N.csv → RevenueNDDPNDVAN"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_int(row.get('Year'))
                year = _safe_int(row.get('Year'))
                records.append(RevenueNDDPNDVAN(
                    year=year,
                    district=row.get('District', '').strip() if row.get('District') else None,
                    crops=_safe_float(row.get('Crops')),
                    livestock=_safe_float(row.get('Livestock')),
                    forestry_and_logging=_safe_float(row.get('Forestry and Logging')),
                    fishing_and_aquaculture=_safe_float(row.get('Fishing and aquaculture')),
                    agriculture_allied_activities=_safe_float(row.get('Agriculture & Allied Activities')),
                    mining_quarrying=_safe_float(row.get('Mining & Quarrying')),
                    primary_sector=_safe_float(row.get('Primary Sector')),
                    manufacturing=_safe_float(row.get('Manufacturing')),
                    electricity_gas_water_supply_other_utility_services=_safe_float(row.get('Electricity, Gas, Water Supply  & Other Utility\nServices')),
                    construction=_safe_float(row.get('Construction')),
                    secondary_sector=_safe_float(row.get('Secondary Sector')),
                    industry=_safe_float(row.get('Industry')),
                    trade_repair_and_hospitality=_safe_float(row.get('Trade, Repair, and Hospitality')),
                    railways=_safe_float(row.get('Railways')),
                    transport_other_than_railways=_safe_float(row.get('Transport (Other than Railways)')),
                    storage=_safe_float(row.get('Storage')),
                    communication_and_broadcast_services=_safe_float(row.get('Communication and Broadcast Services')),
                    financial_services=_safe_float(row.get('Financial Services')),
                    real_estate_other_dwellings_and_professional_services=_safe_float(row.get('Real Estate, Other Dwellings, and Professional Services')),
                    public_administration_and_defence=_safe_float(row.get('Public Administration and Defence')),
                    other_services=_safe_float(row.get('Other Services')),
                    services_tertiary_sector=_safe_float(row.get('Services/ Tertiary Sector')),
                    ndva=_safe_float(row.get('NDVA')),
                    taxes_on_products=_safe_float(row.get('Taxes on products')),
                    less_subsidies_on_products=_safe_float(row.get('Less subsidies on\nproducts')),
                    nddp=_safe_float(row.get('NDDP')),
                    population_000=_safe_float(row.get("Population ('000)")),
                    per_capita_district_domestic_product=_safe_float(row.get('Per capita District Domestic Product')),
                ))
        RevenueNDDPNDVAN.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

