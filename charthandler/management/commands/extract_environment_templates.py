"""
Management command to create/update Chart Templates for the Environment chapter.
Charts matching https://indiandistricts.in/statistics/maharashtra/<district>/environment/
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate

ICRISAT_SOURCE = 'International Crops Research Institute for the Semi-Arid Tropics (ICRISAT)'
DSA_SOURCE = 'District Statistical Abstracts'
NCMRWF_SOURCE = 'National Centre For Medium Range Weather Forecasting'

def build_chart_options(
    y_axis_title,
    x_axis_title='Year',
    is_percent=False,
    disable_all_filter1=False,
    disable_all_filter2=False,
):
    options = {
        'scales': {
            'x': {'title': {'display': True, 'text': x_axis_title}},
            'y': {'beginAtZero': True, 'title': {'display': True, 'text': y_axis_title}},
        }
    }
    if is_percent:
        options['is_percentage_format'] = True
    if disable_all_filter1:
        options['disable_all_filter1'] = True
    if disable_all_filter2:
        options['disable_all_filter2'] = True
    return options

def get_monthly_dataset_config():
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    colors = ['#1a4570', '#e9ba5d', '#e46e53', '#af7c50', '#7a9e7e', '#4c6c9b', '#b38b4d', '#c25a40', '#956842', '#638568', '#38527a', '#8b6938']
    return [{'label': m.capitalize(), 'borderColor': c, 'backgroundColor': c} for m, c in zip(months, colors)]

class Command(BaseCommand):
    help = 'Creates/Updates Chart Templates for the Environment chapter.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Environment...\n')

        templates = [
            # ==================================================================
            # SECTION 1: CLIMATE & ATMOSPHERE
            # ==================================================================
            {
                'title': 'A. Rainfall (Yearly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvRainfall',
                'x_column': 'year',
                'y_columns': ['total'],
                'dataset_config': [
                    {'label': 'Total', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Rainfall (mm)'),
                'description': 'International Crops Research Institute for the Semi-Arid Tropics (ICRISAT)',
                'additional_info': '',
                'display_order': 1,
            },
            {
                'title': 'B. Rainfall (Monthly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvRainfall',
                'x_column': 'year',
                'y_columns': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
                'dataset_config': get_monthly_dataset_config(),
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Rainfall'),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 2,
            },
            {
                'title': 'C. No. of Rainy Days in the Year (Taluka-wise)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvRainyDays',
                'x_column': 'year',
                'y_columns': ['rainy_days_in_year'],
                'dataset_config': [
                    {'label': 'Number of rainy days in the given year', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number of rainy days'),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 3,
            },
            {
                'title': 'D. Evapotranspiration Potential vs Actual Numbers (Yearly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvEvapotranspirationYearly',
                'x_column': 'year',
                'y_columns': ['potential', 'actual_numbers'],
                'dataset_config': [
                    {'label': 'Potential', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Actual Numbers', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Amount (mm)'),
                'description': " International Crops Research Institute for the Semi-Arid Tropics (ICRISAT)",
                'additional_info': "Evapotranspiration refers to the combined processes which move water from the Earth's surface (open water and ice surfaces, bare soil and vegetation) into the atmosphere.",
                'display_order': 4,
            },
            {
                'title': 'E. Annual Runoff',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvRunoff',
                'x_column': 'year',
                'y_columns': ['yearly_runoff'],
                'dataset_config': [
                    {'label': 'Yearly Runoff', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Runoff (mm)'),
                'description': " International Crops Research Institute for the Semi-Arid Tropics (ICRISAT)",
                'additional_info': "Runoff is rain or melted snow that can’t soak into the ground, so it flows across the land into streams and rivers.",
                'display_order': 5,
            },
            {
                'title': 'F. Runoff (Monthly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvRunoff',
                'x_column': 'year',
                'y_columns': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
                'dataset_config': get_monthly_dataset_config(),
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Runoff (mm)'),
                'description': " International Crops Research Institute for the Semi-Arid Tropics (ICRISAT)",
                'additional_info': 'Runoff is rain or melted snow that can’t soak into the ground, so it flows across the land into streams and rivers.',
                'display_order': 6,
            },
            {
                'title': 'G. Water Deficit (Yearly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvWaterDeficit',
                'x_column': 'year',
                'y_columns': ['yearly_water_deficit'],
                'dataset_config': [
                    {'label': 'Yearly Water Deficit', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Deficit Amount (mm)'),
                'description': ICRISAT_SOURCE,
                'additional_info': 'Water deficit is the shortfall between the water plants could use (potential evapotranspiration) and the water actually available to them; it signals how much moisture is missing to meet those atmospheric demands.',
                'display_order': 7,
            },
            {
                'title': 'H. Water Deficit (Monthly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvWaterDeficit',
                'x_column': 'year',
                'y_columns': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'october', 'november', 'december'],
                'dataset_config': [c for c in get_monthly_dataset_config() if c['label'] != 'September'],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Water Deficit'),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 8,
            },
            {
                'title': 'I. Soil Moisture (Yearly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvSoilMoisture',
                'x_column': 'year',
                'y_columns': ['moisture_04mm_1mm', 'moisture_1mm_2mm'],
                'dataset_config': [
                    {'label': '0.4 mm - 1 mm', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': '1 mm - 2mm', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Soil Moisture'),
                'description': NCMRWF_SOURCE,
                'additional_info': 'Soil moisture is measured here as a fraction of water per unit soil volume, expressed in m³/m³.',
                'display_order': 9,
            },
            {
                'title': 'J. Seasonal Groundwater Levels: Bore Wells',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvBorewells',
                'x_column': 'year',
                'y_columns': ['values'],
                'dataset_config': [
                    {'label': 'Groundwater Level', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'season',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Groundwater Level (m)',disable_all_filter1=True),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 10,
            },
            {
                'title': 'K. Seasonal Groundwater Levels: Dug Wells',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvDugwells',
                'x_column': 'year',
                'y_columns': ['values'],
                'dataset_config': [
                    {'label': 'Groundwater Level', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'season',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Groundwater Level (m)',disable_all_filter1=True),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 11,
            },
            {
                'title': 'A. Maximum Temperature (Yearly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvMaxTemperature',
                'x_column': 'year',
                'y_columns': ['max'],
                'dataset_config': [
                    {'label': 'Max', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Temperature (°C)'),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 12,
            },
            {
                'title': 'B. Maximum Temperature (Monthly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvMaxTemperature',
                'x_column': 'year',
                'y_columns': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
                'dataset_config': get_monthly_dataset_config(),
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Max Temperature (°C)'),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 13,
            },
            {
                'title': 'C. Minimum Temperature (Yearly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvMinTemperature',
                'x_column': 'year',
                'y_columns': ['min'],
                'dataset_config': [
                    {'label': 'Min', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Temperature (°C)'),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 14,
            },
            {
                'title': 'D. Minimum Temperature (Monthly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvMinTemperature',
                'x_column': 'year',
                'y_columns': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
                'dataset_config': get_monthly_dataset_config(),
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Min Temperature (°C)'),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 15,
            },
            {
                'title': 'E. Wind Speed (Yearly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvWindSpeed',
                'x_column': 'year',
                'y_columns': ['average'],
                'dataset_config': [
                    {'label': 'Average', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Average Wind Speed (m/s)'),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 16,
            },
            {
                'title': 'F. Wind Speed (Monthly)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvWindSpeed',
                'x_column': 'year',
                'y_columns': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
                'dataset_config': get_monthly_dataset_config(),
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Wind Speed (m/s)'),
                'description': ICRISAT_SOURCE,
                'additional_info': '',
                'display_order': 17,
            },
            {
                'title': 'G. Relative Humidity',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvHumidity',
                'x_column': 'year',
                'y_columns': ['relative_humidity'],
                'dataset_config': [
                    {'label': 'Relative Humidity', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Relative Humidity',is_percent=True),
                'description': NCMRWF_SOURCE,
                'additional_info': '',
                'display_order': 18,
            },

            # ==================================================================
            # SECTION 2: FORESTS & ECOLOGY
            # ==================================================================
            {
                'title': 'A. Forest Area',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvForestArea',
                'x_column': 'year',
                'y_columns': ['forest_area'],
                'dataset_config': [
                    {'label': 'Forest Area', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'area_classification',
                'filter2_column': 'jurisdiction',
                'show_filters': True,
                'chart_options': build_chart_options('Forest Area (sq.km)',disable_all_filter1=True,disable_all_filter2=True),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 19,
            },
            {
                'title': 'B. Forest Area (Filter by Density)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvForestDensity',
                'x_column': 'year',
                'y_columns': ['forest_area'],
                'dataset_config': [
                    {'label': 'Forest Area', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Forest Area (sq.km)',disable_all_filter1=True),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 20,
            },
            {
                'title': 'C. Wildlife Projects (Area and Expenses)',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvWildlifeProjects',
                'x_column': 'year',
                'y_columns': ['value'],
                'dataset_config': [
                    {'label': 'Values', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_wildlife_project',
                'filter2_column': 'project_area_expenses',
                'show_filters': True,
                'chart_options': build_chart_options('Values',disable_all_filter1=True,disable_all_filter2=True),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 21,
            },

            # ==================================================================
            # SECTION 3: HUMAN FOOTPRINT
            # ==================================================================
            {
                'title': 'A. Nighttime Lights',
                'chapter_type': 'environment',
                'chart_type': 'line',
                'data_source_table': 'EnvNightLightIntensity',
                'x_column': 'year',
                'y_columns': ['night_light_intensity'],
                'dataset_config': [
                    {'label': 'Night Light Intensity', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Light Intensity (in lumens)'),
                'description': 'International Crops Research Institute for the Semi-Arid Tropics (ICRISAT)',
                'additional_info': '',
                'display_order': 22,
            },
        ]

        count_new = 0
        count_updated = 0

        for config in templates:
            obj, created = ChartTemplate.objects.update_or_create(
                title=config['title'],
                chapter_type=config['chapter_type'],
                defaults=config,
            )
            if created:
                count_new += 1
                self.stdout.write(f'  [NEW] {obj.title}')
            else:
                count_updated += 1
                self.stdout.write(f'  [UPD] {obj.title}')

        expected_titles = {config['title'] for config in templates}
        stale = list(
            ChartTemplate.objects
            .filter(chapter_type='environment')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale:
            self.stdout.write(self.style.WARNING(
                '\\nStale environment templates (not in this command):\\n'
                + '\\n'.join(f'  - {t}' for t in stale)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\\nDone! {len(templates)} templates processed. ({count_new} new, {count_updated} updated)'
        ))
