"""
Management command to create the default Chart Templates for Industry.
Charts Aâ€“N matching https://indiandistricts.in/statistics/maharashtra/<district>/industry/
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate


EC_SOURCE = 'Economic Census, MoSPI'
DSA_SOURCE = 'District Statistical Abstracts'
FACTORY_SOURCE = 'Directorate of Industrial Safety and Health, Maharashtra'


def build_chart_options(y_axis_title, is_percent=False, disable_all_filter1=False, disable_all_filter2=False, x_axis_title='Year'):
    options = {
        'scales': {
            'x': {'title': {'display': True, 'text': x_axis_title}},
            'y': {'beginAtZero': True, 'title': {'display': True, 'text': y_axis_title}}
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
    help = 'Creates/Updates Chart Templates for the Industry chapter.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Industry...')

        templates = [
            {
                'title': 'A. Number of Establishments',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'ECNumber',
                'x_column': 'year',
                'y_columns': ['number_of_establishments'],
                'dataset_config': [
                    {'label': 'Number of Establishments', 'backgroundColor': '#1E3D59'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': '',
                'additional_info': EC_SOURCE,
                'display_order': 1,
            },

            {
                'title': 'B. Social Group of Establishment Owner',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'ECSocialGroup',
                'x_column': 'year',
                'y_columns': ['sc', 'st', 'obc', 'others'],
                'dataset_config': [
                    {'label': 'SC', 'backgroundColor': '#1E3D59'},
                    {'label': 'ST', 'backgroundColor': '#E5A93B'},
                    {'label': 'OBC', 'backgroundColor': '#C84B31'},
                    {'label': 'Others', 'backgroundColor': '#8D6240'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': EC_SOURCE,
                'additional_info': '',
                'display_order': 2,
            },

            {
                'title': 'C. Sources of Finance',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'ECSourcesOfFinance',
                'x_column': 'year',
                'y_columns': ['self_financed', 'borrowings_and_other_assistance'],
                'dataset_config': [
                    {'label': 'Self-Financed', 'backgroundColor': '#1E3D59'},
                    {'label': 'Borrowings and Other Assistance', 'backgroundColor': '#E5A93B'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Establishments'),
                'description': EC_SOURCE,
                'additional_info': '"Borrowings and assistance" includes establishments financed through borrowings '
                    'from institutional and non-institutional sources, financial assistance from government '
                    'schemes, loans from self-help groups (SHGs), donations or transfers, and other sources.',
                'display_order': 3,
            },

            {
                'title': 'D. Sources of Borrowings and Financial Assistance',
                'chapter_type': 'industry',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'ECSourcesOfBorrowings',
                'x_column': 'year',
                'y_columns': [
                    'borrowing_from_institutions',
                    'borrowing_from_non_institutions',
                    'financial_assistance_from_govt',
                    'donations_transfers',
                    'loans_from_shgs',
                    'others',
                ],
                'dataset_config': [
                    {'label': 'Borrowing from Institutions', 'backgroundColor': '#1E3D59'},
                    {'label': 'Borrowing from Non-Institutions', 'backgroundColor': '#E5A93B'},
                    {'label': 'Financial Assistance from Govt. sources', 'backgroundColor': '#C84B31'},
                    {'label': 'Donations/Transfers', 'backgroundColor': '#8D6240'},
                    {'label': 'Loans from SHGs', 'backgroundColor': '#808080'},
                    {'label': 'Others', 'backgroundColor': '#4A90E2'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Percentage Share (%)', is_percent=True),
                'description': EC_SOURCE,
                'additional_info': ('In 1998 and 2005, sources include borrowings from institutions, non-institutions, '
                    'and financial assistance from govt. sources/schemes, and other sources. '
                    'In the 2013 Economic Census, additional categories: loans from self-help groups (SHGs) '
                    'and donations/transfers were introduced as separate columns. '
                    'These new categories are reflected in the 2013 bar.'),
                'display_order': 4,
            },

            {
                'title': 'E. Government Establishments and PSUs',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'ECType',
                'x_column': 'year',
                'y_columns': ['govt_psu'],
                'dataset_config': [
                    {'label': 'Govt/PSU Establishments', 'backgroundColor': '#1E3D59'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': EC_SOURCE,
                'additional_info': '',
                'display_order': 5,
            },

            {
                'title': 'F. Cooperatives',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'ECType',
                'x_column': 'year',
                'y_columns': ['cooperative'],
                'dataset_config': [
                    {'label': 'Cooperative Establishments', 'backgroundColor': '#1E3D59'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': EC_SOURCE,
                'additional_info': '',
                'display_order': 6,
            },

            {
                'title': 'G. Private Sector Establishments',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'ECType',
                'x_column': 'year',
                'y_columns': ['private_sector'],
                'dataset_config': [
                    {'label': 'Private Sector Establishments', 'backgroundColor': '#1E3D59'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': EC_SOURCE,
                'additional_info': 'The private sector category includes the total of all the following types of '
                    'establishments: Private Proprietary, Private Partnership, Private Company, '
                    'Private SHG, Private Non-Profit, Private Others, Corporate Financial, '
                    'and Corporate Non-Financial.',
                'display_order': 7,
            },


            # J. MSME Industries  (H = Religion, I = Night Lights â€” external data)
            {
                'title': 'J. MSME Industries',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'DSAMsme',
                'x_column': 'year',
                'y_columns': ['number_of_msme_industries'],
                'dataset_config': [
                    {'label': 'Number of MSME Industries', 'backgroundColor': '#1E3D59'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number'),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 10,
            },

            # K. Number of Factory Workers in Registered Factories
            {
                'title': 'K. Number of Factory Workers in Registered Factories',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'FactoryWorkers',
                'x_column': 'manufacturing_category',
                'y_columns': ['num_workers'],
                'dataset_config': [
                    {'label': 'No. of Workers', 'backgroundColor': '#1E3D59'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Workers', x_axis_title='Manufacturing Category'),
                'description': FACTORY_SOURCE,
                'additional_info': 'Values are as of 2023.',
                'display_order': 11,
            },

            # L. Industrial Power Consumption
            {
                'title': 'L. Industrial Power Consumption',
                'chapter_type': 'industry',
                'chart_type': 'line',
                'data_source_table': 'DSAElectricity',
                'x_column': 'year',
                'y_columns': ['industrial_power_consumption'],
                'dataset_config': [
                    {'label': 'Industrial Power Consumption', 'borderColor': '#1E3D59'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Power Consumed (in kWh)'),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 12,
            },

            # M. Pollution Categories
            {
                'title': 'M. Pollution Categories',
                'chapter_type': 'industry',
                'chart_type': 'line',
                'data_source_table': 'DSAPollutionCategory',
                'x_column': 'year',
                'y_columns': ['number_of_industries'],
                'dataset_config': [
                    {'label': 'No. of Industries', 'borderColor': '#1E3D59'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'pollution_category',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Industries', disable_all_filter1=True),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 13,
            },

            {
                'title': 'N. Broad Activities Establishments are Engaged In',
                'chapter_type': 'industry',
                'chart_type': 'bar',
                'data_source_table': 'ECBroadActivity',
                'x_column': 'year',
                'y_columns': [
                    'agriculture_and_allied_activities',
                    'industry',
                    'services',
                ],
                'dataset_config': [
                    {'label': 'Agriculture and Allied Activities', 'backgroundColor': '#1E3D59'},
                    {'label': 'Industry', 'backgroundColor': '#E5A93B'},
                    {'label': 'Services', 'backgroundColor': '#C84B31'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Establishments', disable_all_filter1=True),
                'description': EC_SOURCE,
                'additional_info': (
                    'Agriculture and Allied Activities: Activities relating to agriculture other than crop '
                    'production, Livestock, Forestry and Logging, Fishing and Aquaculture. '
                    'Industry: Mining and Quarrying, Manufacturing, Electricity, Gas, Steam and Air '
                    'Conditioning Supply, Water Supply, Sewerage, Waste Management and Remediation, '
                    'and Construction. '
                    'Services: Wholesale and Retail Trade & Repair of Motor Vehicles, Wholesale Trade, '
                    'Retail Trade, Transportation and Storage, Accommodation and Food Service Activities, '
                    'Information & Communication, Financial and Insurance Activities, Real Estate '
                    'Activities, Professional, Scientific & Technical Activities, Administrative and '
                    'Support Service Activities, Education, Human Health & Social Work Activities, '
                    'Arts, Entertainment, Sports & Amusement and Recreation, Community, Social and '
                    'Personal Services, and Other Service Activities Not Elsewhere Classified.'
                ),
                'display_order': 14,
            },
        ]

        count = 0
        updated = 0
        for config in templates:
            obj, created = ChartTemplate.objects.update_or_create(
                title=config['title'],
                chapter_type=config['chapter_type'],
                defaults=config
            )
            if created:
                count += 1
                self.stdout.write(f'  [NEW] {obj.title}')
            else:
                updated += 1
                self.stdout.write(f'  [UPD] {obj.title}')

        expected_titles = {config['title'] for config in templates}
        stale_titles = list(
            ChartTemplate.objects
            .filter(chapter_type='industry')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale_titles:
            self.stdout.write(self.style.WARNING(
                '\nStale industry templates found (not touched by this command):\n'
                + '\n'.join(f'  - {title}' for title in stale_titles)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Processed {len(templates)} templates. ({count} new, {updated} updated)'
        ))
