"""
Management command to create/update Chart Templates for the Police chapter.
Charts matching http://127.0.0.1:8000/statistics/maharashtra/<district>/police-judiciary/

Reference mapping: Police/Original Data/police_reference.xlsx
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate


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
    help = 'Creates/Updates Chart Templates for the Police chapter.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Police...\n')

        templates = [
            # ==================================================================
            # SECTION 1: CRIMINAL CASES
            # ==================================================================
            {
                'title': 'A. Cognizable Crimes under the Indian Penal Code (IPC)',
                'chapter_type': 'police-judiciary',
                'chart_type': 'line',
                'data_source_table': 'PoliceIPCTotal',
                'x_column': 'year',
                'y_columns': ['cognizable_ipc_crimes'],
                'dataset_config': [
                    {'label': 'Cognizable IPC crimes', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': 'Aggregate total of all cognizable IPC crimes per district per year.',
                'display_order': 1,
            },
            {
                'title': 'B. Select Offenses affecting the Human Body',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceIPCHumanBody',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'crime',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 2,
            },
            {
                'title': 'C. Select Offenses against Property',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceIPCProperty',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'crime',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 3,
            },
            {
                'title': 'D. Select Offenses against Public Tranquility',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceIPCPublicTranquility',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'crime',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 4,
            },
            {
                'title': 'E. Select Offenses relating to Documents and Property Marks',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceIPCDocPropertyMarks',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_offense',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 5,
            },
            {
                'title': 'F. Select Miscellaneous Crimes under the IPC',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceIPCMisc',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_offense',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 6,
            },
            {
                'title': 'G. Cognizable Crimes under Special and Local Laws (SLL)',
                'chapter_type': 'police-judiciary',
                'chart_type': 'line',
                'data_source_table': 'PoliceSLLTotal',
                'x_column': 'year',
                'y_columns': ['cognizable_sll_crimes'],
                'dataset_config': [
                    {'label': 'Cognizable SLL Crimes', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': 'Aggregate total of all cognizable SLL crimes.',
                'display_order': 7,
            },
            {
                'title': 'H. Select Offenses under Special and Local Laws (SLL)',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceSLLOffenseTypes',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_offense_under',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 8,
            },
            {
                'title': 'I. Crimes against Women',
                'chapter_type': 'police-judiciary',
                'chart_type': 'line',
                'data_source_table': 'PoliceWomenTotal',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': 'Aggregate total crimes against women.',
                'display_order': 9,
            },
            {
                'title': 'J. Select Cases of Crimes against Women',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceWomenCrimeTypes',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'crime',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 10,
            },
            {
                'title': 'K. Cyber Crime',
                'chapter_type': 'police-judiciary',
                'chart_type': 'line',
                'data_source_table': 'PoliceCyberTotals',
                'x_column': 'year',
                'y_columns': ['cyber_crimes', 'fraud', 'offenses_under_it_act'],
                'dataset_config': [
                    {'label': 'Cyber Crimes', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Fraud', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Offenses under IT Act', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': 'Aggregate cyber crime totals.',
                'display_order': 11,
            },
            {
                'title': 'L. Select Cases of Cyber Crime',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceCyberCrimeTypes',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'crime',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 12,
            },
            {
                'title': 'M. Cases of Fraud',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceCyberFraudTypes',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_offense',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'National Crime Records Bureau (NCRB)',
                'additional_info': '',
                'display_order': 13,
            },
            {
                'title': 'N. Reported Crimes against Women and Children',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceDSAWomenChildrenTaluka',
                'x_column': 'year',
                'y_columns': ['rape', 'kidnapping_and_abduction', 'dowry_cases', 'sexual_assault'],
                'dataset_config': [
                    {'label': 'Rape', 'backgroundColor': '#1a4570'},
                    {'label': 'Kidnapping and Abduction', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Dowry Cases', 'backgroundColor': '#e46e53'},
                    {'label': 'Sexual Assault', 'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'District Statistical Abstract (DSA)',
                'additional_info': '',
                'display_order': 14,
            },

            # ==================================================================
            # SECTION 2: POLICE INFRASTRUCTURE AND WORKFORCE
            # ==================================================================
            {
                'title': 'A. Police Infrastructure',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceInfrastructure',
                'x_column': 'year',
                'y_columns': ['number'],
                'dataset_config': [
                    {'label': 'Number', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_type_of_police_establishment',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Number'),
                'description': 'District Statistical Abstract (DSA)',
                'additional_info': '',
                'display_order': 15,
            },
            {
                'title': 'B. Police Officers and Employees',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceEmployees',
                'x_column': 'year',
                'y_columns': ['number_of_officers_employees'],
                'dataset_config': [
                    {'label': 'Number of Officers/Employees', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'establishment',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Number'),
                'description': 'District Statistical Abstract (DSA)',
                'additional_info': '',
                'display_order': 16,
            },

            # ==================================================================
            # SECTION 3: JUDICIAL SYSTEM
            # ==================================================================
            {
                'title': 'A. Number of Functioning Courts',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceCourtsFunctioning',
                'x_column': 'year',
                'y_columns': ['functioning_courts'],
                'dataset_config': [
                    {'label': 'Functioning Courts', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type_of_court',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Courts'),
                'description': 'District Statistical Abstract (DSA)',
                'additional_info': '',
                'display_order': 17,
            },
            {
                'title': 'B. Judge Positions',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceCourtsJudgesCases',
                'x_column': 'year',
                'y_columns': ['approved_judge_posts', 'judge_positions_filled'],
                'dataset_config': [
                    {'label': 'Approved Judge Posts', 'backgroundColor': '#1a4570'},
                    {'label': 'Judge Positions Filled', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type_of_court',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Positions'),
                'description': 'District Statistical Abstract (DSA)',
                'additional_info': '',
                'display_order': 18,
            },
            {
                'title': 'C. Cases Resolved',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceCourtsJudgesCases',
                'x_column': 'year',
                'y_columns': ['total_cases'],
                'dataset_config': [
                    {'label': 'Total Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type_of_court',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'District Statistical Abstract (DSA)',
                'additional_info': '',
                'display_order': 19,
            },
            {
                'title': 'D. Number of Original Cases Resolved',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceCourtsOriginalCases',
                'x_column': 'year',
                'y_columns': ['regular', 'miscellaneous', 'all_original_cases'],
                'dataset_config': [
                    {'label': 'Regular', 'backgroundColor': '#1a4570'},
                    {'label': 'Miscellaneous', 'backgroundColor': '#e9ba5d'},
                    {'label': 'All Original Cases', 'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type_of_court',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'District Statistical Abstract (DSA)',
                'additional_info': '',
                'display_order': 20,
            },
            {
                'title': 'E. Number of Appeal Cases Resolved',
                'chapter_type': 'police-judiciary',
                'chart_type': 'bar',
                'data_source_table': 'PoliceCourtsAppealCases',
                'x_column': 'year',
                'y_columns': ['regular', 'miscellaneous', 'all_appeal_cases'],
                'dataset_config': [
                    {'label': 'Regular', 'backgroundColor': '#1a4570'},
                    {'label': 'Miscellaneous', 'backgroundColor': '#e9ba5d'},
                    {'label': 'All Appeal Cases', 'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type_of_court',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Cases'),
                'description': 'District Statistical Abstract (DSA)',
                'additional_info': '',
                'display_order': 21,
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
        # Warn about any stale police templates not in this list
        # ------------------------------------------------------------------
        expected_titles = {config['title'] for config in templates}
        stale = list(
            ChartTemplate.objects
            .filter(chapter_type='police-judiciary')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale:
            self.stdout.write(self.style.WARNING(
                '\nStale police templates (not in this command):\n'
                + '\n'.join(f'  - {t}' for t in stale)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(templates)} templates processed. ({count_new} new, {count_updated} updated)'
        ))
