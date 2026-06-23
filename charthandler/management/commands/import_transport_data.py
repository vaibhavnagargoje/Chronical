"""
Management command to import transport CSV data into the database.

Usage:
    python manage.py import_transport_data [--data-dir PATH] [--clear]

Default data directory: Transport/ in the project root.
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

CSV_MAP = {
    'ARC_Accidents.csv': ('charthandler.TransportARCAccidents', {
        'Fatal Accidents': 'fatal_accidents',
        'Grievous Accidents': 'grievous_accidents',
        'Minor Accidents': 'minor_accidents',
        'Accidents with No Injury': 'accidents_no_injury',
    }),
    'ARC_Age.csv': ('charthandler.TransportARCAge', {
        'Age': 'age',
        'Male': 'male',
        'Female': 'female',
    }),
    'ARC_CaseFine.csv': ('charthandler.TransportARCCaseFine', {
        'Select Violation': 'violation',
        'Number of Cases': 'cases',
        'Fine Collected': 'fine_collected',
    }),
    'ARC_Fatalities.csv': ('charthandler.TransportARCFatalities', {
        'No. of accidents': 'no_of_accidents',
        'Males Killed': 'males_killed',
        'Females Killed': 'females_killed',
        'Total Killed': 'total_killed',
    }),
    'ARC_GrievousInjuries.csv': ('charthandler.TransportARCGrievousInjuries', {
        'No. of accidents': 'no_of_accidents',
        'Males Grievously Injured': 'males_injured',
        'Females Grievously Injured': 'females_injured',
        'Total Grievously Injured': 'total_injured',
    }),
    'ARC_Injuries.csv': ('charthandler.TransportARCInjuries', {
        'Sex': 'sex',
        'Fatalities': 'fatalities',
        'Grievous Injuries': 'grievous_injuries',
        'Minor Injuries': 'minor_injuries',
    }),
    'ARC_MinorInjuries.csv': ('charthandler.TransportARCMinorInjuries', {
        'No. of accidents': 'no_of_accidents',
        'Males Minor Injured': 'males_injured',
        'Females Minor Injured': 'females_injured',
        'Total Minor Injured': 'total_injured',
    }),
    'ARC_ModeTransport.csv': ('charthandler.TransportARCModeTransport', {
        'Fatalities': 'fatalities',
        'Pedestrians': 'pedestrians',
        'Bicycles': 'bicycles',
        'Two- wheeler (Driver)': 'two_wheeler_driver',
        'Two- wheeler (Passenger)': 'two_wheeler_passenger',
        'Three-wheeler': 'three_wheeler',
        'Car, Taxi, and LMV': 'car_taxi_lmv',
        'Buses': 'buses',
        'Trucks/Lorries': 'trucks_lorries',
        'Others': 'others',
    }),
    'ARC_Month.csv': ('charthandler.TransportARCMonth', {
        'Month': 'month',
        'Crash Type': 'crash_type',
        'Number of Crashes': 'number_of_crashes',
    }),
    'ARC_RoadType.csv': ('charthandler.TransportARCRoadType', {
        'Road Type': 'road_type',
        'Fatalities': 'fatalities',
        'Grievous injuries': 'grievous_injuries',
    }),
    'ARC_Time.csv': ('charthandler.TransportARCTime', {
        'Time of Day': 'time_of_day',
        'Fatalities': 'fatalities',
        'Grievous injuries': 'grievous_injuries',
    }),
    'ARC_TotalsInjuryDeath.csv': ('charthandler.TransportARCTotalsInjuryDeath', {
        'Accidents with NO injury': 'accidents_no_injury',
        'Accidents': 'accidents',
        'Persons Killed Or Injured': 'persons_killed_injured',
    }),
    'DSA_100sqkm.csv': ('charthandler.TransportDSA100sqkm', {
        'Taluka': 'taluka',
        'Length of roads per 100 sq.km': 'length_of_roads',
    }),
    'DSA_Bus.csv': ('charthandler.TransportDSABus', {
        'Routes': 'routes',
        'Length of Routes': 'length_of_routes',
        'Average Length of Routes': 'avg_length',
        'Existing Buses': 'existing_buses',
        'Buses Running on the Road': 'buses_running',
        'Daily Avg Passengers (lakh)': 'daily_avg_passengers_lakh',
        'Daily Average Number of Passengers': 'daily_avg_passengers',
        'Revenue from Transportation (lakh)': 'revenue_lakh',
        'Revenue from Transportation': 'revenue',
        'Average Earnings per Passenger': 'avg_earnings_per_passenger',
    }),
    'DSA_Magazine.csv': ('charthandler.TransportDSAMagazine', {
        'Taluka': 'taluka',
        'Daily': 'daily',
        'Weekly': 'weekly',
        'Fortnightly': 'fortnightly',
        'Monthly': 'monthly',
        'Quarterly': 'quarterly',
        'Yearly': 'yearly',
    }),
    'DSA_RoadMaterial.csv': ('charthandler.TransportDSARoadMaterial', {
        'Taluka': 'taluka',
        'Road Material': 'road_material',
        'Length': 'length',
    }),
    'DSA_RoadType.csv': ('charthandler.TransportDSARoadType', {
        'Taluka': 'taluka',
        'Road Type': 'road_type',
        'Length': 'length',
    }),
    'TC Assets.csv': ('charthandler.TransportTCAssets', {
        'Rural/Urban': 'rural_urban',
        'Banking Services': 'banking',
        'Radio/Transistor': 'radio',
        'Television': 'television',
        'Computer/Laptop': 'computer',
        'Computer/Laptop With Internet': 'computer_internet',
        'Computer/Laptop  Without Internet': 'computer_no_internet',
        'Telephone': 'telephone',
        'Landline only': 'landline_only',
        'Mobile only': 'mobile_only',
        'Both Landline and Mobile': 'both_phones',
        'Bicycle': 'bicycle',
        'Scooter/Motorcycle/Moped': 'scooter_motorcycle',
        'Car/Jeep/Van': 'car_jeep',
        'Access to Any Asset': 'access_any',
        'None of the Specified Assets': 'none_specified',
    }),
}

STRING_FIELDS = {
    'age', 'violation', 'sex', 'month', 'crash_type', 'road_type', 'time_of_day', 'taluka', 'road_material', 'rural_urban'
}

class Command(BaseCommand):
    help = 'Import transport CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir', type=str,
            default=os.path.join(settings.BASE_DIR, 'Transport'),
            help='Path to the directory containing transport CSV files',
        )
        parser.add_argument(
            '--clear', action='store_true',
            help='Clear existing transport data before importing',
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing from: {data_dir}')

        model_cache = {}
        for csv_file, (model_path, _) in CSV_MAP.items():
            app_label, model_name = model_path.rsplit('.', 1)
            model_cache[csv_file] = apps.get_model(app_label, model_name)

        if options['clear']:
            self.stdout.write('Clearing existing transport data...')
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
                kwargs['district'] = row.get('District', '').strip()

                year = row.get('Year')
                if year is not None and str(year).strip() != '':
                    year_val = _safe_float(year)
                    if year_val is not None:
                        kwargs['year'] = int(year_val)
                    else:
                        kwargs['year'] = None
                else:
                    kwargs['year'] = None

                for csv_col, model_field in col_map.items():
                    raw = row.get(csv_col, '')
                    if model_field in STRING_FIELDS:
                        kwargs[model_field] = str(raw).strip() if raw else ''
                    else:
                        kwargs[model_field] = _safe_float(raw)

                records.append(ModelClass(**kwargs))

        ModelClass.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
