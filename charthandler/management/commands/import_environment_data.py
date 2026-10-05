"""
Management command to import environment data into the database.

Usage:
    python manage.py import_environment_data [--data-dir PATH] [--clear]

Default data directory: Environment/ in the project root.
"""
import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from charthandler.models import (
    EnvWildlifeProjects,
    EnvForestArea,
    EnvForestDensity,
    EnvNightLightIntensity,
    EnvRunoff,
    EnvRainyDays,
    EnvRainfall,
    EnvMinTemperature,
    EnvMaxTemperature,
    EnvWindSpeed,
    EnvWaterDeficit,
    EnvHumidity,
    EnvSoilMoisture,
    EnvEvapotranspirationYearly,
    EnvEvapotranspirationMonthly,
    EnvBorewells,
    EnvDugwells,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_float(value):
    """Safely convert a value to float, returning None for empty/invalid."""
    if value is None:
        return None
    s = str(value).strip()
    if s in ('', 'nan', 'NaN', 'None'):
        return None
    try:
        return float(s.replace(',', ''))
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    """Safely convert a value to int via float, returning None for empty/invalid."""
    f = _safe_float(value)
    if f is None:
        return None
    return int(f)


def _str(value, default=''):
    """Get a stripped string, defaulting to ''."""
    if value is None:
        return default
    s = str(value).strip()
    return s if s not in ('nan', 'NaN', 'None') else default


# ---------------------------------------------------------------------------
# All models (for --clear)
# ---------------------------------------------------------------------------

ALL_MODELS = [
    EnvWildlifeProjects,
    EnvForestArea,
    EnvForestDensity,
    EnvNightLightIntensity,
    EnvRunoff,
    EnvRainyDays,
    EnvRainfall,
    EnvMinTemperature,
    EnvMaxTemperature,
    EnvWindSpeed,
    EnvWaterDeficit,
    EnvHumidity,
    EnvSoilMoisture,
    EnvEvapotranspirationYearly,
    EnvEvapotranspirationMonthly,
    EnvBorewells,
    EnvDugwells,
]


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = 'Import environment data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Environment'),
            help='Path to the directory containing environment xlsx files (default: Environment/)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing environment data before importing',
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']

        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing environment data from: {data_dir}\n')

        if options['clear']:
            self.stdout.write('Clearing existing environment data...')
            for ModelClass in ALL_MODELS:
                deleted, _ = ModelClass.objects.all().delete()
                self.stdout.write(f'  Cleared {deleted:>6} rows from {ModelClass.__name__}')
            self.stdout.write(self.style.SUCCESS('All environment data cleared.\n'))

        xlsx_importers = [
            ('wildlife_projects.xlsx',              self._import_wildlife_projects),
            ('forest_area_(dsa).xlsx',              self._import_forest_area),
            ('forest_density_(dsa).xlsx',           self._import_forest_density),
            ('night_light_intensity_(icrisat.xlsx', self._import_night_light_intensity),
            ('runoff_(icrisat).xlsx',               self._import_runoff),
            ('rainy_days_(dsa).xlsx',               self._import_rainy_days),
            ('rainfall_(icrisat).xlsx',             self._import_rainfall),
            ('min_temperature_(icrisat.xlsx',       self._import_min_temperature),
            ('max_temperature_(icrisat).xlsx',      self._import_max_temperature),
            ('wind_speed_(icrisat).xlsx',           self._import_wind_speed),
            ('water_deficit_(icrisat).xlsx',        self._import_water_deficit),
            ('humidity.xlsx',                       self._import_humidity),
            ('soil_moisture.xlsx',                  self._import_soil_moisture),
            ('evapotranspiration_yearly.xlsx',      self._import_evapotranspiration_yearly),
            ('evapotranspiration_monthly.xlsx',     self._import_evapotranspiration_monthly),
            ('borewells.xlsx',                      self._import_borewells),
            ('dugwells.xlsx',                       self._import_dugwells),
        ]

        total_records = 0
        for filename, importer in xlsx_importers:
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

    def _read_xlsx(self, filepath):
        """Read an xlsx file into a list of dicts."""
        df = pd.read_excel(filepath, dtype=str)
        df = df.fillna('')
        return df.to_dict(orient='records')

    def _import_wildlife_projects(self, filepath):
        """wildlife_projects.xlsx → EnvWildlifeProjects"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvWildlifeProjects(
                year=year,
                district=_str(row.get('District')),
                select_wildlife_project=_str(row.get('Select Wildlife Project')),
                project_area_expenses=_str(row.get('Project Area/Expenses')),
                value=_safe_float(row.get('Value')),
            ))
        EnvWildlifeProjects.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_forest_area(self, filepath):
        """forest_area_(dsa).xlsx → EnvForestArea"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvForestArea(
                year=year,
                district=_str(row.get('District')),
                area_classification=_str(row.get('Area Classification')),
                jurisdiction=_str(row.get('Jurisdiction')),
                forest_area=_safe_float(row.get('Forest Area')),
            ))
        EnvForestArea.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_forest_density(self, filepath):
        """forest_density_(dsa).xlsx → EnvForestDensity"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvForestDensity(
                year=year,
                district=_str(row.get('District')),
                type=_str(row.get('Type')),
                forest_area=_safe_float(row.get('Forest Area')),
            ))
        EnvForestDensity.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_night_light_intensity(self, filepath):
        """night_light_intensity_(icrisat.xlsx → EnvNightLightIntensity"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvNightLightIntensity(
                year=year,
                district=_str(row.get('District')),
                night_light_intensity=_safe_float(row.get('Night Light Intensity')),
            ))
        EnvNightLightIntensity.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_runoff(self, filepath):
        """runoff_(icrisat).xlsx → EnvRunoff (long format: District, Year, Month, Runoff, Yearly Runoff)"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            month = _str(row.get('Month'))
            if year is None or not month:
                continue
            records.append(EnvRunoff(
                year=year,
                district=_str(row.get('District')),
                month=month,
                runoff=_safe_float(row.get('Runoff')),
                yearly_runoff=_safe_float(row.get('Yearly Runoff')),
            ))
        EnvRunoff.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_rainy_days(self, filepath):
        """rainy_days_(dsa).xlsx → EnvRainyDays"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvRainyDays(
                year=year,
                district=_str(row.get('District')),
                taluka=_str(row.get('Taluka')),
                avg_rainy_days=_safe_float(row.get('Average number of rainy days')),
                rainy_days_in_year=_safe_float(row.get('Number of rainy days in the given year')),
                precipitation_in_year=_safe_float(row.get('Percipitation in the given year')),
            ))
        EnvRainyDays.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_rainfall(self, filepath):
        """rainfall_(icrisat).xlsx → EnvRainfall (long format: District, Year, Month, Rainfall, Total)"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            month = _str(row.get('Month'))
            if year is None or not month:
                continue
            records.append(EnvRainfall(
                year=year,
                district=_str(row.get('District')),
                month=month,
                rainfall=_safe_float(row.get('Rainfall')),
                total=_safe_float(row.get('Total')),
            ))
        EnvRainfall.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_min_temperature(self, filepath):
        """min_temperature_(icrisat.xlsx → EnvMinTemperature (long format: District, Year, Month, Min Temperature, Min)"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            month = _str(row.get('Month'))
            if year is None or not month:
                continue
            records.append(EnvMinTemperature(
                year=year,
                district=_str(row.get('District')),
                month=month,
                min_temperature=_safe_float(row.get('Min Temperature')),
                min=_safe_float(row.get('Min')),
            ))
        EnvMinTemperature.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_max_temperature(self, filepath):
        """max_temperature_(icrisat).xlsx → EnvMaxTemperature (long format: District, Year, Month, Max Temperature, Max)"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            month = _str(row.get('Month'))
            if year is None or not month:
                continue
            records.append(EnvMaxTemperature(
                year=year,
                district=_str(row.get('District')),
                month=month,
                max_temperature=_safe_float(row.get('Max Temperature')),
                max=_safe_float(row.get('Max')),
            ))
        EnvMaxTemperature.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_wind_speed(self, filepath):
        """wind_speed_(icrisat).xlsx → EnvWindSpeed (long format: District, Year, Month, Wind Speed, Average)"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            month = _str(row.get('Month'))
            if year is None or not month:
                continue
            records.append(EnvWindSpeed(
                year=year,
                district=_str(row.get('District')),
                month=month,
                wind_speed=_safe_float(row.get('Wind Speed')),
                average=_safe_float(row.get('Average')),
            ))
        EnvWindSpeed.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_water_deficit(self, filepath):
        """water_deficit_(icrisat).xlsx → EnvWaterDeficit (long format: District, Year, Month, Water Deficit, Yearly Water Deficit)"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            month = _str(row.get('Month'))
            if year is None or not month:
                continue
            records.append(EnvWaterDeficit(
                year=year,
                district=_str(row.get('District')),
                month=month,
                water_deficit=_safe_float(row.get('Water Deficit')),
                yearly_water_deficit=_safe_float(row.get('Yearly Water Deficit')),
            ))
        EnvWaterDeficit.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_humidity(self, filepath):
        """humidity.xlsx → EnvHumidity"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvHumidity(
                year=year,
                district=_str(row.get('District')),
                relative_humidity=_safe_float(row.get('Relative Humidity')),
            ))
        EnvHumidity.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_soil_moisture(self, filepath):
        """soil_moisture.xlsx → EnvSoilMoisture"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvSoilMoisture(
                year=year,
                district=_str(row.get('District')),
                moisture_1mm_2mm=_safe_float(row.get('1 mm - 2mm')),
                moisture_04mm_1mm=_safe_float(row.get('0.4 mm - 1 mm')),
            ))
        EnvSoilMoisture.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_evapotranspiration_yearly(self, filepath):
        """evapotranspiration_yearly.xlsx → EnvEvapotranspirationYearly"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvEvapotranspirationYearly(
                year=year,
                district=_str(row.get('District')),
                actual_numbers=_safe_float(row.get('Actual Numbers')),
                potential=_safe_float(row.get('Potential')),
            ))
        EnvEvapotranspirationYearly.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_evapotranspiration_monthly(self, filepath):
        """evapotranspiration_monthly.xlsx → EnvEvapotranspirationMonthly
        Long format: District, Year, Month, Actual ET, Potential ET
        """
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            month = _str(row.get('Month'))
            if year is None or not month:
                continue
            records.append(EnvEvapotranspirationMonthly(
                year=year,
                district=_str(row.get('District')),
                month=month,
                actual_et=_safe_float(row.get('Actual ET')),
                potential_et=_safe_float(row.get('Potential ET')),
            ))
        EnvEvapotranspirationMonthly.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_borewells(self, filepath):
        """borewells.xlsx → EnvBorewells (ignore unnamed/empty columns)"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvBorewells(
                year=year,
                district=_str(row.get('District')),
                season=_str(row.get('Season')),
                values=_safe_float(row.get('values')),
            ))
        EnvBorewells.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_dugwells(self, filepath):
        """dugwells.xlsx → EnvDugwells"""
        records = []
        for row in self._read_xlsx(filepath):
            year = _safe_int(row.get('Year'))
            if year is None:
                continue
            records.append(EnvDugwells(
                year=year,
                district=_str(row.get('District')),
                season=_str(row.get('Season')),
                values=_safe_float(row.get('values')),
            ))
        EnvDugwells.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
