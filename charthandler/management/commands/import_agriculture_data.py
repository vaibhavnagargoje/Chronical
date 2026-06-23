"""
Management command to import agriculture CSV data into the database.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from charthandler.models.agriculture import (
    AgcGrosscroppedarea,
    AgcHoldingsarea,
    AgcHoldingsnumber,
    AgcLanduse,
    DsaChemicalfertilizer,
    DsaIrrigationbeneficiary,
    DsaIrrigationfacilities,
    DsaIrrigationprojects,
    DsaIrrigationwells,
    DsaTubewellshandpumps,
)

def _safe_float(value):
    if value is None or str(value).strip() in ('', 'nan', 'NaN', 'None'):
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

def _str(row, col):
    return str(row.get(col, '') or '').strip()

ALL_MODELS = [
    AgcGrosscroppedarea,
    AgcHoldingsarea,
    AgcHoldingsnumber,
    AgcLanduse,
    DsaChemicalfertilizer,
    DsaIrrigationbeneficiary,
    DsaIrrigationfacilities,
    DsaIrrigationprojects,
    DsaIrrigationwells,
    DsaTubewellshandpumps,
]

class Command(BaseCommand):
    help = 'Import agriculture CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Agriculture'),
            help='Path to the directory containing agriculture CSV files (default: Agriculture/)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing agriculture data before importing',
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']

        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing agriculture data from: {data_dir}\n')

        if options['clear']:
            self.stdout.write('Clearing existing agriculture data...')
            for ModelClass in ALL_MODELS:
                deleted, _ = ModelClass.objects.all().delete()
                self.stdout.write(f'  Cleared {deleted:>6} rows from {ModelClass.__name__}')
            self.stdout.write(self.style.SUCCESS('All agriculture data cleared.\n'))

        csv_importers = [
            ('AGC_GrossCroppedArea.csv', self._import_agc_grosscroppedarea),
            ('AGC_HoldingsArea.csv', self._import_agc_holdingsarea),
            ('AGC_HoldingsNumber.csv', self._import_agc_holdingsnumber),
            ('AGC_LandUse.csv', self._import_agc_landuse),
            ('DSA_ChemicalFertilizer.csv', self._import_dsa_chemicalfertilizer),
            ('DSA_IrrigationBeneficiary.csv', self._import_dsa_irrigationbeneficiary),
            ('DSA_IrrigationFacilities.csv', self._import_dsa_irrigationfacilities),
            ('DSA_IrrigationProjects.csv', self._import_dsa_irrigationprojects),
            ('DSA_IrrigationWells.csv', self._import_dsa_irrigationwells),
            ('DSA_TubewellsHandpumps.csv', self._import_dsa_tubewellshandpumps),
        ]

        total_records = 0
        for filename, importer in csv_importers:
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'  [SKIP] {filename} - file not found'))
                continue
            try:
                count = importer(filepath)
                total_records += count
                self.stdout.write(self.style.SUCCESS(f'  [OK]   {filename} - {count} records'))
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f'  [ERROR] {filename}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'\nImport complete! Total records imported: {total_records}'))

    def _import_agc_grosscroppedarea(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(AgcGrosscroppedarea(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    size_class=_str(row, 'Size Class'),
                    irrigated_area=_safe_float(row.get('Irrigated Area')),
                    unirrigated_area=_safe_float(row.get('Unirrigated Area')),
                    gross_cropped_area=_safe_float(row.get('Gross Cropped Area')),
                    share_of_cropped_area_irrigated=_safe_float(row.get('Share of Cropped Area Irrigated')),
                    share_of_total_land_holdings_cropped=_safe_float(row.get('Share of Total Land Holdings Cropped')),
                    unnamed_9=_safe_float(row.get('Unnamed: 9')),
                    total_holding_number=_safe_float(row.get('Total Holding Number')),
                    total_holding_area=_safe_float(row.get('Total Holding Area')),
                ))
        AgcGrosscroppedarea.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_agc_holdingsarea(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(AgcHoldingsarea(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    marginal_below_1_ha=_safe_float(row.get('Marginal (Below 1 ha)')),
                    small_1_to_2_ha=_safe_float(row.get('Small (1 to 2 ha)')),
                    semimedium_2_to_4_ha=_safe_float(row.get('Semimedium (2 to 4 ha)')),
                    medium_4_to_10_ha=_safe_float(row.get('Medium (4 to 10 ha)')),
                    large_10_ha=_safe_float(row.get('Large (>10 ha)')),
                ))
        AgcHoldingsarea.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_agc_holdingsnumber(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(AgcHoldingsnumber(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    marginal_below_1_ha=_safe_float(row.get('Marginal (Below 1 ha)')),
                    small_1_to_2_ha=_safe_float(row.get('Small (1 to 2 ha)')),
                    semimedium_2_to_4_ha=_safe_float(row.get('Semimedium (2 to 4 ha)')),
                    medium_4_to_10_ha=_safe_float(row.get('Medium (4 to 10 ha)')),
                    large_10_ha=_safe_float(row.get('Large (>10 ha)')),
                ))
        AgcHoldingsnumber.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_agc_landuse(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(AgcLanduse(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    size_class=_str(row, 'Size Class'),
                    total_holdings_number=_safe_float(row.get('Total Holdings Number')),
                    total_holdings_area=_safe_float(row.get('Total Holdings Area')),
                    area_classified_as_cultivated=_safe_float(row.get('Area Classified as Cultivated')),
                    area_classified_as_uncultivated=_safe_float(row.get('Area Classified as Uncultivated')),
                    area_not_available_for_agriculture=_safe_float(row.get('Area Not Available For Agriculture')),
                    net_sown_area=_safe_float(row.get('Net Sown Area')),
                    current_fallow=_safe_float(row.get('Current Fallow')),
                    actually_uncultivated_area=_safe_float(row.get('Actually Uncultivated Area')),
                    other_fallow_land=_safe_float(row.get('Other Fallow Land')),
                    cultivable_waste_land=_safe_float(row.get('Cultivable Waste Land')),
                ))
        AgcLanduse.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_chemicalfertilizer(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DsaChemicalfertilizer(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    kharif=_safe_float(row.get('Kharif')),
                    rabi=_safe_float(row.get('Rabi')),
                ))
        DsaChemicalfertilizer.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_irrigationbeneficiary(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                    
                irr_ben_area = _safe_float(row.get('Irrigation Beneficiary Area'))
                irr_area = _safe_float(row.get('Irrigated Area'))
                
                share = _safe_float(row.get('Share of Beneficiary Area Irrigated'))
                if share is None and irr_ben_area and irr_area is not None:
                    if irr_ben_area > 0:
                        share = (irr_area / irr_ben_area) * 100
                    else:
                        share = 0.0

                records.append(DsaIrrigationbeneficiary(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    project_size=_str(row, 'Project Size'),
                    irrigation_beneficiary_area=irr_ben_area,
                    irrigated_area=irr_area,
                    share_of_beneficiary_area_irrigated=share,
                ))
        DsaIrrigationbeneficiary.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_irrigationfacilities(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DsaIrrigationfacilities(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    ponds_or_village_lakes=_safe_float(row.get('Ponds or Village Lakes')),
                    storage_dams=_safe_float(row.get('Storage Dams')),
                    irrigation_wells=_safe_float(row.get('Irrigation Wells')),
                    diesel_pumps=_safe_float(row.get('Diesel Pumps')),
                    electric_pumps=_safe_float(row.get('Electric Pumps')),
                ))
        DsaIrrigationfacilities.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_irrigationprojects(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DsaIrrigationprojects(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    small_local=_safe_float(row.get('Small (Local)')),
                    small_state=_safe_float(row.get('Small (State)')),
                    medium=_safe_float(row.get('Medium')),
                    big=_safe_float(row.get('Big')),
                ))
        DsaIrrigationprojects.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_irrigationwells(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DsaIrrigationwells(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    total_irrigation_wells=_safe_float(row.get('Total Irrigation Wells')),
                    wells_in_use_with_diesel_pump=_safe_float(row.get('Wells In Use With Diesel Pump')),
                    wells_in_use_with_electric_pump=_safe_float(row.get('Wells In Use With Electric Pump')),
                    irrigation_wells_not_in_use=_safe_float(row.get('Irrigation Wells Not in Use')),
                ))
        DsaIrrigationwells.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dsa_tubewellshandpumps(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DsaTubewellshandpumps(
                    year=year,
                    district=_str(row, 'District'),
                    taluka=_str(row, 'Taluka'),
                    all_tubewells=_safe_float(row.get('All Tubewells')),
                    high_capacity_tubewells=_safe_float(row.get('High Capacity Tubewells')),
                    successful_tubewells=_safe_float(row.get('Successful Tubewells')),
                    hand_pumps=_safe_float(row.get('Hand Pumps')),
                    electric_pumps=_safe_float(row.get('Electric Pumps')),
                ))
        DsaTubewellshandpumps.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)


