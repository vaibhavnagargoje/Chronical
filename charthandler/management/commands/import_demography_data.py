"""
Management command to import demography CSV data into the database.

Usage:
    python manage.py import_demography_data [--data-dir PATH] [--clear]

Default data directory: Demography/ in the project root.

CSV files expected (matching sheet names from Demography.xlsx):
    Census_Population.csv
    Census_SC.csv
    Census_ST.csv
    Census_AgeDist.csv
    Census_Literate.csv
    Census_Working.csv
    Census_InwardMigration_A.csv
    Census_InwardMigration_B.csv
    Census_InwardMigrationC.csv
    Census_InwardMigrationD.csv
    Census_InwardMigration_E.csv
    Census_MotherTongue.csv
    Census_Religion.csv
    Census_SexRatio.csv
    Census_ToiletFacility.csv
    Census_Cooking.csv
    Census_Water.csv
    Census_Electricity.csv
    Census_TC.csv
    Census_Ownership.csv
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from charthandler.models import (
    CensusPopulation,
    CensusSC,
    CensusST,
    CensusAgeDistribution,
    CensusLiterate,
    CensusWorking,
    CensusInwardMigrationA,
    CensusInwardMigrationB,
    CensusInwardMigrationC,
    CensusInwardMigrationD,
    CensusInwardMigrationE,
    CensusMotherTongue,
    CensusReligion,
    CensusSexRatio,
    CensusToiletFacility,
    CensusCooking,
    CensusWater,
    CensusElectricity,
    CensusTCAssets,
    CensusOwnership,
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
    CensusPopulation,
    CensusSC,
    CensusST,
    CensusAgeDistribution,
    CensusLiterate,
    CensusWorking,
    CensusInwardMigrationA,
    CensusInwardMigrationB,
    CensusInwardMigrationC,
    CensusInwardMigrationD,
    CensusInwardMigrationE,
    CensusMotherTongue,
    CensusReligion,
    CensusSexRatio,
    CensusToiletFacility,
    CensusCooking,
    CensusWater,
    CensusElectricity,
    CensusTCAssets,
    CensusOwnership,
]


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = 'Import demography CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Demography'),
            help='Path to the directory containing demography CSV files (default: Demography/)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing demography data before importing',
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']

        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing demography data from: {data_dir}\n')

        # --clear: delete all rows from every demography model
        if options['clear']:
            self.stdout.write('Clearing existing demography data...')
            for ModelClass in ALL_MODELS:
                deleted, _ = ModelClass.objects.all().delete()
                self.stdout.write(f'  Cleared {deleted:>6} rows from {ModelClass.__name__}')
            self.stdout.write(self.style.SUCCESS('All demography data cleared.\n'))

        # Map: csv filename  →  importer method name
        csv_importers = [
            ('Census_Population.csv',        self._import_population),
            ('Census_SC.csv',                self._import_sc),
            ('Census_ST.csv',                self._import_st),
            ('Census_AgeDist.csv',           self._import_age_dist),
            ('Census_Literate.csv',          self._import_literate),
            ('Census_Working.csv',           self._import_working),
            ('Census_InwardMigration_A.csv', self._import_migration_a),
            ('Census_InwardMigration_B.csv', self._import_migration_b),
            ('Census_InwardMigrationC.csv',  self._import_migration_c),
            ('Census_InwardMigrationD.csv',  self._import_migration_d),
            ('Census_InwardMigration_E.csv', self._import_migration_e),
            ('Census_MotherTongue.csv',      self._import_mother_tongue),
            ('Census_Religion.csv',          self._import_religion),
            ('Census_SexRatio.csv',          self._import_sex_ratio),
            ('Census_ToiletFacility.csv',    self._import_toilet_facility),
            ('Census_Cooking.csv',           self._import_cooking),
            ('Census_Water.csv',             self._import_water),
            ('Census_Electricity.csv',       self._import_electricity),
            ('Census_TC.csv',                self._import_tc_assets),
            ('Census_Ownership.csv',         self._import_ownership),
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
    # Individual importers — one per CSV / model
    # -------------------------------------------------------------------------

    def _import_population(self, filepath):
        """Census_Population.csv → CensusPopulation"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusPopulation(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    total=_safe_float(row.get('Total')),
                    male=_safe_float(row.get('Male')),
                    female=_safe_float(row.get('Female')),
                ))
        CensusPopulation.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_sc(self, filepath):
        """Census_SC.csv → CensusSC"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusSC(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    population=_safe_float(row.get('Population')),
                    male=_safe_float(row.get('Male')),
                    female=_safe_float(row.get('Female')),
                ))
        CensusSC.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_st(self, filepath):
        """Census_ST.csv → CensusST"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusST(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    population=_safe_float(row.get('Population')),
                    male=_safe_float(row.get('Male')),
                    female=_safe_float(row.get('Female')),
                ))
        CensusST.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_age_dist(self, filepath):
        """Census_AgeDist.csv → CensusAgeDistribution"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusAgeDistribution(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    age_group=_str(row, 'Age Group'),
                    population=_safe_float(row.get('Population')),
                    male=_safe_float(row.get('Male')),
                    female=_safe_float(row.get('Female')),
                ))
        CensusAgeDistribution.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_literate(self, filepath):
        """Census_Literate.csv → CensusLiterate"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusLiterate(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    literate_population=_safe_float(row.get('Literate Population')),
                    male=_safe_float(row.get('Male')),
                    female=_safe_float(row.get('Female')),
                ))
        CensusLiterate.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_working(self, filepath):
        """Census_Working.csv → CensusWorking"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusWorking(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    working_population=_safe_float(row.get('Working Population')),
                    male=_safe_float(row.get('Male')),
                    female=_safe_float(row.get('Female')),
                    main_worker_population=_safe_float(row.get('Main Worker Population')),
                    male_main_workers=_safe_float(row.get('Male Main Workers')),
                    female_main_workers=_safe_float(row.get('Female Main Workers')),
                    marginal_worker_population=_safe_float(row.get('Marginal Worker Population')),
                    male_marginal_workers=_safe_float(row.get('Male Marginal Workers')),
                    female_marginal_workers=_safe_float(row.get('Female Marginal Workers')),
                ))
        CensusWorking.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_migration(self, filepath, ModelClass):
        """Generic importer for all 5 InwardMigration sheets (same columns)."""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(ModelClass(
                    year=year,
                    district=_str(row, 'District'),
                    birth_place=_str(row, 'Birth Place'),
                    population=_safe_float(row.get('Population')),
                    male=_safe_float(row.get('Male')),
                    female=_safe_float(row.get('Female')),
                    rural_population=_safe_float(row.get('Rural Population')),
                    rural_male=_safe_float(row.get('Rural Male')),
                    rural_female=_safe_float(row.get('Rural Female')),
                    urban_population=_safe_float(row.get('Urban Population')),
                    urban_male=_safe_float(row.get('Urban Male')),
                    urban_female=_safe_float(row.get('Urban Female')),
                ))
        ModelClass.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_migration_a(self, filepath):
        """Census_InwardMigration_A.csv → CensusInwardMigrationA"""
        return self._import_migration(filepath, CensusInwardMigrationA)

    def _import_migration_b(self, filepath):
        """Census_InwardMigration_B.csv → CensusInwardMigrationB"""
        return self._import_migration(filepath, CensusInwardMigrationB)

    def _import_migration_c(self, filepath):
        """Census_InwardMigrationC.csv → CensusInwardMigrationC"""
        return self._import_migration(filepath, CensusInwardMigrationC)

    def _import_migration_d(self, filepath):
        """Census_InwardMigrationD.csv → CensusInwardMigrationD"""
        return self._import_migration(filepath, CensusInwardMigrationD)

    def _import_migration_e(self, filepath):
        """Census_InwardMigration_E.csv → CensusInwardMigrationE"""
        return self._import_migration(filepath, CensusInwardMigrationE)

    def _import_mother_tongue(self, filepath):
        """Census_MotherTongue.csv → CensusMotherTongue"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusMotherTongue(
                    year=year,
                    district=_str(row, 'District'),
                    mother_tongue=_str(row, 'Mother Tongue'),
                    male=_safe_float(row.get('Male')),
                    female=_safe_float(row.get('Female')),
                ))
        CensusMotherTongue.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_religion(self, filepath):
        """Census_Religion.csv → CensusReligion"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusReligion(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    gender=_str(row, 'Gender'),
                    buddhist=_safe_float(row.get('Buddhist')),
                    christian=_safe_float(row.get('Christian')),
                    hindu=_safe_float(row.get('Hindu')),
                    jain=_safe_float(row.get('Jain')),
                    muslim=_safe_float(row.get('Muslim')),
                    sikh=_safe_float(row.get('Sikh')),
                    other=_safe_float(row.get('Other')),
                    not_stated=_safe_float(row.get('Not Stated')),
                ))
        CensusReligion.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_sex_ratio(self, filepath):
        """Census_SexRatio.csv → CensusSexRatio"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusSexRatio(
                    year=year,
                    district=_str(row, 'District'),
                    sex_ratio=_safe_float(row.get('Sex Ratio')),
                ))
        CensusSexRatio.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_toilet_facility(self, filepath):
        """Census_ToiletFacility.csv → CensusToiletFacility"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusToiletFacility(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    pit_latrine=_safe_float(row.get('Pit Latrine')),
                    water_closet=_safe_float(row.get('Water Closet')),
                    other=_safe_float(row.get('Other')),
                    no_latrine=_safe_float(row.get('No Latrine')),
                ))
        CensusToiletFacility.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_cooking(self, filepath):
        """Census_Cooking.csv → CensusCooking"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusCooking(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    firewood=_safe_float(row.get('Fire-wood')),
                    crop_residue=_safe_float(row.get('Crop residue')),
                    cowdung_cake=_safe_float(row.get('Cowdung Cake')),
                    coal_lignite_charcoal=_safe_float(row.get('Coal, Lignite, Charcoal')),
                    kerosene=_safe_float(row.get('Kerosene')),
                    lpg_png=_safe_float(row.get('LPG/PNG')),
                    electricity=_safe_float(row.get('Electricity')),
                    biogas=_safe_float(row.get('Biogas')),
                    other=_safe_float(row.get('Other')),
                    no_cooking=_safe_float(row.get('No cooking')),
                ))
        CensusCooking.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_water(self, filepath):
        """Census_Water.csv → CensusWater"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusWater(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    location=_str(row, 'Location'),
                    tap=_safe_float(row.get('Tap')),
                    handpump=_safe_float(row.get('Handpump')),
                    tubewell=_safe_float(row.get('Tubewell')),
                    well=_safe_float(row.get('Well')),
                    all_others=_safe_float(row.get('All Others')),
                ))
        CensusWater.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_electricity(self, filepath):
        """Census_Electricity.csv → CensusElectricity"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusElectricity(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    access_to_electricity=_safe_float(row.get('Access to Electricity')),
                    no_access_to_electricity=_safe_float(row.get('No Access to Electricity')),
                ))
        CensusElectricity.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_tc_assets(self, filepath):
        """Census_TC.csv → CensusTCAssets"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusTCAssets(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    banking_services=_safe_float(row.get('Banking Services')),
                    radio_transistor=_safe_float(row.get('Radio/Transistor')),
                    television=_safe_float(row.get('Television')),
                    computer_laptop=_safe_float(row.get('Computer/Laptop')),
                    computer_laptop_with_internet=_safe_float(row.get('Computer/Laptop With Internet')),
                    computer_laptop_without_internet=_safe_float(row.get('Computer/Laptop  Without Internet')),
                    telephone=_safe_float(row.get('Telephone')),
                    households_with_landline=_safe_float(row.get('Households with Landline')),
                    households_with_mobile=_safe_float(row.get('Households with Mobile ')),
                    bicycle=_safe_float(row.get('Bicycle')),
                    scooter_motorcycle_moped=_safe_float(row.get('Scooter/Motorcycle/Moped')),
                    car_jeep_van=_safe_float(row.get('Car/Jeep/Van')),
                    access_to_any_asset=_safe_float(row.get('Access to Any Asset')),
                    none_of_the_specified_assets=_safe_float(row.get('None of the Specified Assets')),
                ))
        CensusTCAssets.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_ownership(self, filepath):
        """Census_Ownership.csv → CensusOwnership"""
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(CensusOwnership(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    owned=_safe_float(row.get('Owned')),
                    rented=_safe_float(row.get('Rented')),
                    other=_safe_float(row.get('Other')),
                ))
        CensusOwnership.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
