"""
Management command to create/update Chart Templates for the Demography chapter.
Charts matching http://127.0.0.1:8000/statistics/maharashtra/<district>/demography/

Reference mapping: Demography/Original Data/Demography_Refrences.xlsx
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate


CENSUS_SOURCE = 'Census of India'


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


class Command(BaseCommand):
    help = 'Creates/Updates Chart Templates for the Demography chapter.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Demography...\n')

        templates = [

            # ==================================================================
            # SECTION 1: POPULATION PROFILE
            # ==================================================================

            # Chart 1 — Population (Census_Population)
            # x=Year, filter=Rural/Urban, y=Total/Male/Female
            {
                'title': 'A. Population',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusPopulation',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male Population',   'backgroundColor': '#1a4570'},
                    {'label': 'Female Population', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population'),
                'description': "Census Tables, accessed through National Data and Analytics Platform (NDAP)",
                'additional_info': '',
                'display_order': 1,
            },

            # Chart 2 — Age Distribution (Census_AgeDist)
            # x=Age Group, filter=Year + Rural/Urban, y=Population/Male/Female
            {
                'title': 'B. Age Distribution of Population',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusAgeDistribution',
                'x_column': 'age_group',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male', 'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'year',
                'filter2_column': 'rural_urban',
                'show_filters': True,
                'chart_options': build_chart_options('Population', x_axis_title='Age Group', disable_all_filter1=True),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 2,
            },

            # Chart 3 — Scheduled Caste Population (Census_SC)
            # x=Year, filter=Rural/Urban, y=Population/Male/Female
            {
                'title': 'C. Scheduled Caste Population',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusSC',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male', 'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population'),
                'description': 'Census Tables, accessed through National Data and Analytics Platform (NDAP)',
                'additional_info': '',
                'display_order': 3,
            },

            # Chart 4 — Scheduled Tribe Population (Census_ST)
            # x=Year, filter=Rural/Urban, y=Population/Male/Female
            {
                'title': 'D. Scheduled Tribe Population',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusST',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male', 'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population'),
                'description': 'Census Tables, accessed through National Data and Analytics Platform (NDAP)',
                'additional_info': '',
                'display_order': 4,
            },

            # Chart 5 — Literate Population (Census_Literate)
            # x=Year, filter=Rural/Urban, y=Literate Population/Male/Female
            {
                'title': 'E. Literate Population',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusLiterate',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male', 'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population'),
                'description': 'Census Tables, accessed through National Data and Analytics Platform (NDAP)',
                'additional_info': 'According to the Census, a person aged seven and above, who can both read and write with understanding in any language, is treated as literate.',
                'display_order': 5,
            },

            # Chart 6 — Working Population (Census_Working)
            # x=Year, filter=Rural/Urban, y=Working Population/Male/Female
            {
                'title': 'F. Working Population',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusWorking',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male',   'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population'),
                'description': 'Census Tables',
                'additional_info': 'The census defines a person as a ‘worker’ when she/he has participated in any economic productive at any time during the reference period (one year preceding the date of enumeration). The working population includes both main workers (who have worked more than 6 months) and marginal workers (who have worked less than 6 months) in the reference period.',
                'display_order': 6,
            },

            # Chart 7 — Mother Tongue (Census_MotherTongue)
            # x=Year, no filter, y=Male/Female
            {
                'title': 'G. Mother Tongue',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusMotherTongue',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male',   'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'mother_tongue',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population', disable_all_filter1=True),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 7,
            },

            # Chart 8 — Religious Composition (Census_Religion)
            # x=Year, filter=Rural/Urban + Gender, y=Buddhist/Christian/Hindu/Jain/Muslim/Sikh/Other/Not Stated
            {
                'title': 'H. Religious Composition of Population',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusReligion',
                'x_column': 'year',
                'y_columns': ['hindu', 'muslim', 'buddhist', 'christian', 'jain', 'sikh', 'other', 'not_stated'],
                'dataset_config': [
                    {'label': 'Hindu',     'backgroundColor': '#1a4570'},
                    {'label': 'Muslim',    'backgroundColor': '#e9ba5d'},
                    {'label': 'Christian', 'backgroundColor': '#e46e53'},
                    {'label': 'Sikh',      'backgroundColor': '#af7c50'},
                    {'label': 'Jain',      'backgroundColor': '#a59f9c'},
                    {'label': 'Buddhist',  'backgroundColor': '#6cbde0'},
                    {'label': 'Other',     'backgroundColor': '#757595'},
                    {'label': 'Not Stated','backgroundColor': '#478db8'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': 'gender',
                'show_filters': True,
                'chart_options': build_chart_options('Population'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 8,
            },

            # Chart 9 — Sex Ratio (Census_SexRatio)
            # x=Year, no filter, y=Sex Ratio
            {
                'title': 'I. Sex Ratio of Population',
                'chapter_type': 'demography',
                'chart_type': 'line',
                'data_source_table': 'CensusSexRatio',
                'x_column': 'year',
                'y_columns': ['sex_ratio'],
                'dataset_config': [
                    {'label': 'Sex Ratio (females per 1000 males)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Females (per thousand males)'),
                'description': 'Health Management Information System (HMIS), accessed through National Data and Analytics Platform (NDAP)',
                'additional_info': '',
                'display_order': 9,
            },

            # ==================================================================
            # SECTION 2: HOUSEHOLD CHARACTERISTICS
            # ==================================================================

            # Chart — Number of Households (placeholder — data source TBD)
            {
                'title': 'A. Number of Households',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': '',
                'x_column': 'year',
                'y_columns': ['total'],
                'dataset_config': [
                    {'label': 'Total Households', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 10,
            },

            # Chart — Household Size (placeholder — data source TBD)
            {
                'title': 'B. Household Size',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': '',
                'x_column': 'year',
                'y_columns': ['household_size'],
                'dataset_config': [
                    {'label': 'Average Household Size', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Persons per Household'),
                'description': 'Census Tables',
                'additional_info': 'Household size is calculated as the total population divided by the number of households.',
                'display_order': 11,
            },

            # Chart — Ownership of Houses (Census_Ownership)
            # x=Year, filter=Rural/Urban, y=Owned/Rented
            {
                'title': 'C. Ownership of Houses',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusOwnership',
                'x_column': 'year',
                'y_columns': ['owned', 'rented'],
                'dataset_config': [
                    {'label': 'Owned',  'backgroundColor': '#1a4570'},
                    {'label': 'Rented', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 12,
            },

            # Chart — Primary Source of Water (Census_Water)
            # x=Year, filter=Rural/Urban + Location, y=Tap/Handpump/Tubewell/Well/All Others
            {
                'title': 'D. Primary Source of Water',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusWater',
                'x_column': 'year',
                'y_columns': ['tap','well', 'handpump', 'tubewell', 'all_others'],
                'dataset_config': [
                    {'label': 'Tap',        'backgroundColor': '#1a4570'},
                    {'label': 'Well',       'backgroundColor': '#e9ba5d'},
                    {'label': 'Handpump',   'backgroundColor': '#e46e53'},
                    {'label': 'Tubewell',   'backgroundColor': '#af7c50'},
                    {'label': 'All Others', 'backgroundColor': '#a59f9c'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households',disable_all_filter1=True),
                'description': 'Census Tables',
                'additional_info': 'In the 2011 Census, Tapwater and Well are divided into treated/untreated and covered/uncovered, while in 2001 they appear as single categories. Here, 2011 values are combined. Also, 2011 reports fewer main water sources. Tanks, ponds, lakes, rivers, canals, and springs are grouped as “Other Sources.”',
                'display_order': 13,
            },

            # Chart 14 — Primary Fuel for Cooking (Census_Cooking)
            # x=Year, filter=Rural/Urban, y=all fuel types
            {
                'title': 'E. Primary Fuel used for Cooking',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusCooking',
                'x_column': 'year',
                'y_columns': ['firewood','lpg_png', 'kerosene','crop_residue', 'cowdung_cake', 'electricity', 'coal_lignite_charcoal',   'biogas', 'other'],
                'dataset_config': [
                    {'label': 'Fire-wood',             'backgroundColor': '#1a4570'},
                    {'label': 'LPG/PNG',               'backgroundColor': '#e9ba5d'},
                    {'label': 'Kerosene',              'backgroundColor': '#e46e53'},
                    {'label': 'Crop Residue',          'backgroundColor': '#af7c50'},
                    {'label': 'Cowdung Cake',          'backgroundColor': '#a59f9c'},
                    {'label': 'Electricity',           'backgroundColor': '#6cbde0'},
                    {'label': 'Coal/Lignite/Charcoal', 'backgroundColor': '#757595'},
                    {'label': 'Biogas',                'backgroundColor': '#478db8'},
                    {'label': 'Other',                 'backgroundColor': '#9c71c6'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 14,
            },

            # Chart — Access to Electricity (Census_Electricity)
            # x=Year, filter=Rural/Urban, y=Access/No Access
            {
                'title': 'F. Access to Electricity',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusElectricity',
                'x_column': 'year',
                'y_columns': ['access_to_electricity', 'no_access_to_electricity'],
                'dataset_config': [
                    {'label': 'Access to Electricity',    'backgroundColor': '#1a4570'},
                    {'label': 'No Access to Electricity', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households',disable_all_filter1=True),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 15,
            },

            # Chart — Availability of Toilet Facilities (Census_ToiletFacility)
            # x=Year, filter=Rural/Urban, y=Pit Latrine/Water Closet/Other/No Latrine
            {
                'title': 'G. Availability of Toilet Facilities',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusToiletFacility',
                'x_column': 'year',
                'y_columns': ['pit_latrine', 'water_closet', 'other', 'no_latrine'],
                'dataset_config': [
                    {'label': 'Pit Latrine',  'backgroundColor': '#1a4570'},
                    {'label': 'Water Closet', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Other',        'backgroundColor': '#e46e53'},
                    {'label': 'No Latrine',   'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '"No Latrine" refers only to households not having a latrine facility within the premises of the house, and covers households that make use of public latrines and open latrines.',
                'display_order': 16,
            },

            # Chart — Ownership of Transportation Assets (Census_TC)
            # x=Year, filter=Rural/Urban, y=Bicycle/Scooter/Car
            {
                'title': 'H. Ownership of Transportation Assets',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusTCAssets',
                'x_column': 'year',
                'y_columns': ['bicycle', 'scooter_motorcycle_moped', 'car_jeep_van'],
                'dataset_config': [
                    {'label': 'Bicycle',                  'backgroundColor': '#1a4570'},
                    {'label': 'Scooter/Motorcycle/Moped', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Car/Jeep/Van',             'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 17,
            },

            # Chart — Access to Communication Assets (Census_TC)
            # x=Year, filter=Rural/Urban, y=Radio/TV/Computer
            {
                'title': 'I. Access to Communication Assets',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusTCAssets',
                'x_column': 'year',
                'y_columns': [ 'households_with_mobile', 'radio_transistor', 'television', 'computer_laptop'],
                'dataset_config': [
                    {'label': 'Telephone',        'backgroundColor': '#1a4570'},
                    {'label': 'Radio/Transistor', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Television',       'backgroundColor': '#e46e53'},
                    {'label': 'Computer/Laptop',  'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 18,
            },

            # Chart — Access to Banking Services (Census_TC)
            # x=Year, filter=Rural/Urban, y=Banking Services
            {
                'title': 'J. Access to Banking Services',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusTCAssets',
                'x_column': 'year',
                'y_columns': ['banking_services'],
                'dataset_config': [
                    {'label': 'Banking Services', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 19,
            },

            # ==================================================================
            # SECTION 3: MIGRATION
            # ==================================================================

            # Chart 20 — Population from within Maharashtra (Census_InwardMigration_B)
            # x=Year, filter=Birth Place, y=Population/Male/Female
            {
                'title': 'A. Population from within Maharashtra',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusInwardMigrationB',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male',   'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'birth_place',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population', disable_all_filter1=True),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 20,
            },

            # Chart 21 — Population from Other States (Census_InwardMigration_D)
            # x=Year, filter=Birth Place (State), y=Population/Male/Female
            {
                'title': 'B. Population from Other States in India',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusInwardMigrationD',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male',   'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'birth_place',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population', disable_all_filter1=True),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 21,
            },

            # Chart 22 — Population from Other Countries (Census_InwardMigration_E)
            # x=Year, filter=Birth Place (Country), y=Population/Male/Female
            {
                'title': 'C. Population from Other Countries',
                'chapter_type': 'demography',
                'chart_type': 'bar',
                'data_source_table': 'CensusInwardMigrationE',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male',   'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'birth_place',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Population', disable_all_filter1=True),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 22,
            },
        ]

        # ------------------------------------------------------------------
        # Create or update each template
        # ------------------------------------------------------------------
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

        # ------------------------------------------------------------------
        # Warn about any stale demography templates not in this list
        # ------------------------------------------------------------------
        expected_titles = {config['title'] for config in templates}
        stale = list(
            ChartTemplate.objects
            .filter(chapter_type='demography')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale:
            self.stdout.write(self.style.WARNING(
                '\nStale demography templates (not in this command):\n'
                + '\n'.join(f'  - {t}' for t in stale)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(templates)} templates processed. ({count_new} new, {count_updated} updated)'
        ))
