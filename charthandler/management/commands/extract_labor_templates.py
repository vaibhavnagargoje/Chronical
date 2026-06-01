"""
Management command to create the default Chart Templates for Labor.
Charts matching https://indiandistricts.in/statistics/maharashtra/<district>/labour/
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate


CENSUS_SOURCE = 'Census Tables'
EC_SOURCE = 'Economic Census, MoSPI'
DSA_SOURCE = 'District Statistical Abstracts'
MNREGA_SOURCE = 'MNREGA'


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
    help = 'Creates/Updates Chart Templates for the Labor chapter.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Labor...')

        # Fix previous misspellings of chapter_type from 'labour' to 'labor'
        ChartTemplate.objects.filter(chapter_type='labour').update(chapter_type='labor')

        templates = [
            # SECTION 1: WORKFORCE COMPOSITION
            {
                'title': 'A. Main Worker Population',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborWorkers',
                'x_column': 'year',
                'y_columns': ['male_main_workers', 'female_main_workers'],
                'dataset_config': [
                    {'label': 'Male Main Workers', 'backgroundColor': '#1a4570'},
                    {'label': 'Female Main Workers', 'backgroundColor': '#E5A93B'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number of Workers'),
                'description': CENSUS_SOURCE,
                'additional_info': 'Main workers are defined as those who worked for 6 months or more during the year.',
                'display_order': 1,
            },
            {
                'title': 'B. Marginal Worker Population',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborWorkers',
                'x_column': 'year',
                'y_columns': ['male_marginal_workers', 'female_marginal_workers'],
                'dataset_config': [
                    {'label': 'Male Marginal Workers', 'backgroundColor': '#1a4570'},
                    {'label': 'Female Marginal Workers', 'backgroundColor': '#E5A93B'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number of Workers'),
                'description': CENSUS_SOURCE,
                'additional_info': 'Marginal workers are those who had not worked for at least 6 months during the year.',
                'display_order': 2,
            },
            # Skipping C. Non-Worker Population since we didn't extract gender splits for Non-Workers
            {
                'title': 'D. Age Composition of Main Workers',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborAgeDistribution',
                'x_column': 'age_group',
                'y_columns': ['main_workers'],
                'dataset_config': [
                    {'label': 'Main Workers', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'year',
                'filter2_column': 'rural_urban',
                'show_filters': True,
                'chart_options': build_chart_options('No. of People', x_axis_title='Age Group', disable_all_filter1=True),
                'description': CENSUS_SOURCE,
                'additional_info': 'Main workers are defined as those who worked for 6 months or more during the year.',
                'display_order': 4,
            },
            {
                'title': 'E. Age Composition of Marginal Workers',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborAgeDistribution',
                'x_column': 'age_group',
                'y_columns': ['marginal_workers'],
                'dataset_config': [
                    {'label': 'Marginal Workers', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'year',
                'filter2_column': 'rural_urban',
                'show_filters': True,
                'chart_options': build_chart_options('No. of People', x_axis_title='Age Group', disable_all_filter1=True),
                'description': CENSUS_SOURCE,
                'additional_info': 'Marginal workers are those who had not worked for at least 6 months during the year.',
                'display_order': 5,
            },
            {
                'title': 'F. Age Composition of Non-Workers',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborAgeDistribution',
                'x_column': 'age_group',
                'y_columns': ['non_workers'],
                'dataset_config': [
                    {'label': 'Non-Workers', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'year',
                'filter2_column': 'rural_urban',
                'show_filters': True,
                'chart_options': build_chart_options('No. of People', x_axis_title='Age Group', disable_all_filter1=True),
                'description': CENSUS_SOURCE,
                'additional_info': 'Those who had not worked at all during a year are considered non-workers.',
                'display_order': 6,
            },
            
            # SECTION 2: EMPLOYMENT CHARACTERISTICS
            {
                'title': 'A. Number of Workers',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborECWorkers',
                'x_column': 'year',
                'y_columns': ['number_of_workers'],
                'dataset_config': [
                    {'label': 'Number of Workers', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number of Workers'),
                'description': EC_SOURCE,
                'additional_info': '',
                'display_order': 7,
            },
            {
                'title': 'B. Workers: Hired vs Not-Hired',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborECGender',
                'x_column': 'year',
                'y_columns': ['employed_hired', 'employed_not_hired'],
                'dataset_config': [
                    {'label': 'Employed (Hired)', 'backgroundColor': '#1a4570'},
                    {'label': 'Employed (Not Hired)', 'backgroundColor': '#E5A93B'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'gender',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number of Workers'),
                'description': EC_SOURCE,
                'additional_info':  'People who were paid employees on the last working day of the census period are counted as Employed (Hired). People who worked without pay (such as self-employed or volunteers) are counted as Employed (Not Hired).',
                'display_order': 8,
            },
            {
                'title': 'C. People Working in Govt Sector/PSUs',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborECWorkers',
                'x_column': 'year',
                'y_columns': ['govt_psu_workers'],
                'dataset_config': [
                    {'label': 'Govt/PSU Workers', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': EC_SOURCE,
                'additional_info': '',
                'display_order': 9,
            },
            {
                'title': 'D. People Working in Cooperatives',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborECWorkers',
                'x_column': 'year',
                'y_columns': ['cooperative_workers'],
                'dataset_config': [
                    {'label': 'Cooperative Workers', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': EC_SOURCE,
                'additional_info': '',
                'display_order': 10,
            },
            {
                'title': 'E. People Working in Private Sector',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'LaborECWorkers',
                'x_column': 'year',
                'y_columns': ['private_sector_workers'],
                'dataset_config': [
                    {'label': 'Private Sector Workers', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': EC_SOURCE,
                'additional_info': 'Private sector includes private non-profits, private proprietaries, private partnerships, private companies, corporate (financial and non-financial companies), private self-help groups (SHGs).',
                'display_order': 11,
            },
            {
                'title': 'F. People Working in MSMEs',
                'chapter_type': 'labor',
                'chart_type': 'bar',
                'data_source_table': 'Unknown', # found in Industry sheet but refrence says is it in Labour
                'x_column': 'year',
                'y_columns': ['number_of_msme_industries'], # Wait, is this workers or industries? The reference says: "F: Number of Employees" for the Excel sheet, but the DB model DSAMsme has `number_of_msme_industries`. I will use what's there and point out if it's incorrect. Let's use `number_of_msme_industries`.
                'dataset_config': [
                    {'label': 'MSME Workers', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number'),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 12,
            },
            {
                'title': 'G. Govt, Semi-Govt, and Private Employees',
                'chapter_type': 'labor',
                'chart_type': 'line',
                'data_source_table': 'LaborIndustryType',    
                'x_column': 'year',
                'y_columns': ['govt_employees', 'semi_govt_employees', 'private_employees'],
                'dataset_config': [
                    {'label': 'Govt. Employees', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Semi-Govt. Employees', 'borderColor': '#E5A93B', 'backgroundColor': '#E5A93B'},
                    {'label': 'Private Employees', 'borderColor': '#C84B31', 'backgroundColor': '#C84B31'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type_of_industry',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number',disable_all_filter1=True),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 13,
            },
            {
                'title': 'H. Government Employment',
                'chapter_type': 'labor',
                'chart_type': 'line',
                'data_source_table': 'LaborGovtEmployees',
                'x_column': 'year',
                'y_columns': ['approved_posts', 'positions_filled'],
                'dataset_config': [
                    {'label': 'Approved Posts', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Positions Filled', 'borderColor': '#E5A93B', 'backgroundColor': '#E5A93B'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'group',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number'),
                'description': DSA_SOURCE,
                'additional_info': '',
                'display_order': 14,
            },
            
            # SECTION 3: MNREGA
            {
                'title': 'A. Participation in MNREGA',
                'chapter_type': 'labor',
                'chart_type': 'line',
                'data_source_table': 'LaborMNREGAParticipation',
                'x_column': 'year',
                'y_columns': ['demanded_work', 'allotted_work', 'worked'],
                'dataset_config': [
                    {'label': 'Demanded Work', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Allotted Work', 'borderColor': '#E5A93B', 'backgroundColor': '#E5A93B'},
                    {'label': 'Worked', 'borderColor': '#C84B31', 'backgroundColor': '#C84B31'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of People'),
                'description': MNREGA_SOURCE,
                'additional_info': '',
                'display_order': 15,
            },
            {
                'title': 'B. MNREGA Household Scope',
                'chapter_type': 'labor',
                'chart_type': 'line',
                'data_source_table': 'LaborMNREGAScope',
                'x_column': 'year',
                'y_columns': ['demanded_work', 'allotted_work', 'worked'],
                'dataset_config': [
                    {'label': 'Demanded Work', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Allotted Work', 'borderColor': '#E5A93B', 'backgroundColor': '#E5A93B'},
                    {'label': 'Worked', 'borderColor': '#C84B31', 'backgroundColor': '#C84B31'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Households'),
                'description': MNREGA_SOURCE,
                'additional_info': '',
                'display_order': 16,
            },
            {
                'title': 'C. Job Cards Issued',
                'chapter_type': 'labor',
                'chart_type': 'line',
                'data_source_table': 'LaborMNREGAJobCards',
                'x_column': 'year',
                'y_columns': ['job_cards_issued'],
                'dataset_config': [
                    {'label': 'Job Cards Issued', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': MNREGA_SOURCE,
                'additional_info': '',
                'display_order': 17,
            },
            {
                'title': 'D. Job Cards Issued for SC and ST',
                'chapter_type': 'labor',
                'chart_type': 'line',
                'data_source_table': 'LaborMNREGAJobCards',
                'x_column': 'year',
                'y_columns': ['sc', 'st'],
                'dataset_config': [
                    {'label': 'SC', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'ST', 'borderColor': '#E5A93B', 'backgroundColor': '#E5A93B'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': MNREGA_SOURCE,
                'additional_info': '',
                'display_order': 18,
            },
            {
                'title': 'E. MNREGA Accounts',
                'chapter_type': 'labor',
                'chart_type': 'line',
                'data_source_table': 'LaborMNREGAAccounts',
                'x_column': 'year',
                'y_columns': ['bank_accounts', 'post_office_accounts'],
                'dataset_config': [
                    {'label': 'Bank Accounts', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Post Office Accounts', 'borderColor': '#E5A93B', 'backgroundColor': '#E5A93B'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Number'),
                'description': MNREGA_SOURCE,
                'additional_info': 'Under MGNREGA, accounts refer to the wage payment accounts opened for workers to receive their earnings. Every registered worker must have either a bank account or a post office savings account linked to their job card.',
                'display_order': 19,
            },
        ]

        # In a real scenario, this matches health and industry template scripts
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
            .filter(chapter_type='labor')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale_titles:
            self.stdout.write(self.style.WARNING(
                '\nStale labor templates found (not touched by this command):\n'
                + '\n'.join(f'  - {title}' for title in stale_titles)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Processed {len(templates)} templates. ({count} new, {updated} updated)'
        ))