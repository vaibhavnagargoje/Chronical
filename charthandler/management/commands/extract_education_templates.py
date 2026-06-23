"""
Management command to create/update Chart Templates for the Education chapter.
Charts matching http://127.0.0.1:8000/statistics/maharashtra/<district>/education/

Reference mapping: Education/Original Data/education_reference_sheet.xlsx
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
    help = 'Creates/Updates Chart Templates for the Education chapter.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Education...\n')

        templates = [
            # ==================================================================
            # SECTION 1: ENROLLMENT AND DROPOUT RATE
            # ==================================================================
            {
                'title': 'A. Student Enrollment Numbers',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'StudentEnrollmentNumbers',
                'x_column': 'year',
                'y_columns': ['primary_school_i_v', 'upper_primary_school_vi_viii', 'secondary_school_ix_x', 'higher_secondary_school_xi_xii'],
                'dataset_config': [
                    {'label': 'Primary School (I-V)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Upper Primary School (VI-VIII)', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Secondary School (IX-X)', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Higher Secondary School (XI-XII)', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'social_category',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Students',disable_all_filter1=True),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 1,
            },
            {
                'title': 'B. Student Enrollment (Class-Wise)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'StudentEnrollmentClassWise',
                'x_column': 'year',
                'y_columns': ['pre_primary', 'class_1', 'class_2', 'class_3', 'class_4', 'class_5', 'class_6', 'class_7', 'class_8', 'class_9', 'class_10', 'class_11', 'class_12'],
                'dataset_config': [
                    {'label': 'Pre-Primary', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Class 1', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Class 2', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Class 3', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                    {'label': 'Class 4', 'borderColor': '#a59f9c', 'backgroundColor': '#a59f9c'},
                    {'label': 'Class 5', 'borderColor': '#6cbde0', 'backgroundColor': '#6cbde0'},
                    {'label': 'Class 6', 'borderColor': '#757595', 'backgroundColor': '#757595'},
                    {'label': 'Class 7', 'borderColor': '#478db8', 'backgroundColor': '#478db8'},
                    {'label': 'Class 8', 'borderColor': '#9c71c6', 'backgroundColor': '#9c71c6'},
                    {'label': 'Class 9', 'borderColor': '#d66a6a', 'backgroundColor': '#d66a6a'},
                    {'label': 'Class 10', 'borderColor': '#3e8f6e', 'backgroundColor': '#3e8f6e'},
                    {'label': 'Class 11', 'borderColor': '#bc995e', 'backgroundColor': '#bc995e'},
                    {'label': 'Class 12', 'borderColor': '#7c5e93', 'backgroundColor': '#7c5e93'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'social_category',
                'filter2_column': 'gender',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Students',disable_all_filter1=True,disable_all_filter2=True),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 2,
            },
            {
                'title': 'C. Student Enrollment (Gender-Wise)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'StudentEnrollmentBoysVsGirls',
                'x_column': 'year',
                'y_columns': ['boys', 'girls'],
                'dataset_config': [
                    {'label': 'Boys', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Girls', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_class',
                'filter2_column': 'social_category',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Students',disable_all_filter2=True),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 3,
            },
            {
                'title': 'D. Student Enrollment (By School Management Type)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'StudentEnrollmentGirlsVsBoys',
                'x_column': 'year',
                'y_columns': ['central_govt', 'government_aided', 'local_body', 'others', 'private_unaided_recognized'],
                'dataset_config': [
                    {'label': 'Central Govt', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Government Aided', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Local Body', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Private Unaided (Recognized)', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                    {'label': 'Others', 'borderColor': '#a59f9c', 'backgroundColor': '#a59f9c'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'gender',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Students'),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 4,
            },
            {
                'title': 'E. Drop Out Rate (By Schooling Level)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'DropOutRateSchoolingStage',
                'x_column': 'year',
                'y_columns': ['primary_i_v', 'upper_primary_vi_viii', 'secondary_ix_x'],
                'dataset_config': [
                    {'label': 'Primary (I-V)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Upper Primary (VI-VIII)', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Secondary (IX-X)', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'social_category',
                'filter2_column': 'gender',
                'show_filters': True,
                'chart_options': build_chart_options('Rate', is_percent=True,disable_all_filter2=True,disable_all_filter1=True),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 5,
            },
            {
                'title': 'F. Drop Out Rate (By Gender)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'DropOutRateByGender',
                'x_column': 'year',
                'y_columns': ['overall', 'boys', 'girls'],
                'dataset_config': [
                    {'label': 'Overall', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Boys', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Girls', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_schooling_level',
                'filter2_column': 'social_category',
                'show_filters': True,
                'chart_options': build_chart_options('Rate', is_percent=True,disable_all_filter1=True,disable_all_filter2=True),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 6,
            },

            # ==================================================================
            # SECTION 2: SCHOOLS
            # ==================================================================
            {
                'title': 'A. No. of Schools',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'NoOfSchoolsType',
                'x_column': 'year',
                'y_columns': ['primary_school_i_v', 'upper_primary_school_i_viii', 'secondary_school_i_x', 'secondary_school_vi_x', 'higher_secondary_school_i_xii'],
                'dataset_config': [
                    {'label': 'Primary School (I-V)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Upper Primary School (I-VIII)', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Secondary School (I-X)', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Secondary School (VI-X)', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                    {'label': 'Higher Secondary School (I-XII)', 'borderColor': '#a59f9c', 'backgroundColor': '#a59f9c'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_school_management_type',
                'filter2_column': 'rural_urban',
                'show_filters': True,
                'chart_options': build_chart_options('Schools'),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 7,
            },
            {
                'title': 'B. No. of Schools (Filtered by Gender Mix)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'NoOfSchools',
                'x_column': 'year',
                'y_columns': ['primary_school_i_v', 'upper_primary_school_i_viii', 'secondary_school_i_x', 'secondary_school_vi_x', 'higher_secondary_school_i_xii'],
                'dataset_config': [
                    {'label': 'Primary School (I-V)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Upper Primary School (I-VIII)', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Secondary School (I-X)', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Secondary School (VI-X)', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                    {'label': 'Higher Secondary School (I-XII)', 'borderColor': '#a59f9c', 'backgroundColor': '#a59f9c'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'gender_mix',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Schools', disable_all_filter1=True),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 8,
            },
            {
                'title': 'C. No. of Schools (By School Management Type)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'NoOfSchoolsManagementType',
                'x_column': 'year',
                'y_columns': ['central_govt', 'government_aided', 'local_body', 'others', 'private_unaided_recognized'],
                'dataset_config': [
                    {'label': 'Central Govt', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Government Aided', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Local Body', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Private Unaided (Recognized)', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                    {'label': 'Others', 'borderColor': '#a59f9c', 'backgroundColor': '#a59f9c'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type_of_school',
                'filter2_column': 'rural_urban',
                'show_filters': True,
                'chart_options': build_chart_options('Schools'),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 9,
            },

            # ==================================================================
            # SECTION 3: TEACHERS
            # ==================================================================
            {
                'title': 'A. No. of Teachers',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'TeacherCategory',
                'x_column': 'year',
                'y_columns': ['primary_school_i_v', 'upper_primary_school_i_viii', 'secondary_school_i_x', 'secondary_school_vi_x', 'higher_secondary_school_i_xii', 'higher_secondary_school_xi_xii'],
                'dataset_config': [
                    {'label': 'Primary School (I-V)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Upper Primary School (I-VIII)', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Secondary School (I-X)', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Secondary School (VI-X)', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                    {'label': 'Higher Secondary School (I-XII)', 'borderColor': '#a59f9c', 'backgroundColor': '#a59f9c'},
                    {'label': 'Higher Secondary School (XI-XII)', 'borderColor': '#6cbde0', 'backgroundColor': '#6cbde0'},
                   
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_school_management_type',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Teachers'),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 10,
            },
            {
                'title': 'B. No. of Teachers (By School Management Type)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'NoOfTeachersByType',
                'x_column': 'year',
                'y_columns': ['central_govt', 'government_aided', 'local_body', 'others', 'private_unaided'],
                'dataset_config': [
                    {'label': 'Central Govt', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Government Aided', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Local Body', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Private Unaided', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                    {'label': 'Others', 'borderColor': '#a59f9c', 'backgroundColor': '#a59f9c'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'type_of_school',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Teachers'),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 11,
            },
            {
                'title': 'C. No. of Teachers (Male vs Female)',
                'chapter_type': 'education',
                'chart_type': 'line',
                'data_source_table': 'TeacherSocialCategory',
                'x_column': 'year',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'select_school_management_type',
                'filter2_column': 'social_category',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Teachers', disable_all_filter1=True, disable_all_filter2=True),
                'description': 'UDISE+',
                'additional_info': '',
                'display_order': 12,
            },
            {
                'title': 'D. Education Level of Teachers',
                'chapter_type': 'education',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'EducationLevels',
                'x_column': 'year',
                'y_columns': ['primary', 'middle', 'matriculation_secondary', 'higher_secondary_intermediate_pre_university_senior_secondary', 'non_technical_diploma_or_certificate_not_equal_to_degree', 'technical_diploma_or_certificate_not_equal_to_degree', 'graduate_and_above'],
                'dataset_config': [
                    {'label': 'Primary', 'backgroundColor': '#1a4570'},
                    {'label': 'Middle', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Matriculation/Secondary', 'backgroundColor': '#e46e53'},
                    {'label': 'Higher Secondary/ Intermediate/ Pre University/ Senior Secondary', 'backgroundColor': '#af7c50'},
                    {'label': 'Non technical diploma or certificate not equal to degree', 'backgroundColor': '#a59f9c'},
                    {'label': 'Technical diploma or certificate not equal to degree', 'backgroundColor': '#6cbde0'},
                    {'label': 'Graduate and above', 'backgroundColor': '#757595'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'age_group',
                'filter2_column': 'gender',
                'show_filters': True,
                'chart_options': build_chart_options('Share of all Teachers', disable_all_filter1=True),
                'description': 'Census Tables',
                'additional_info': 'When filtering by age group, keep in mind 1991 combines ages 15 to 19 into one age group while 2001 and 2011 keep each year separate. Both have been left as is.',
                'display_order': 13,
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
        # Warn about any stale education templates not in this list
        # ------------------------------------------------------------------
        expected_titles = {config['title'] for config in templates}
        stale = list(
            ChartTemplate.objects
            .filter(chapter_type='education')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale:
            self.stdout.write(self.style.WARNING(
                '\nStale education templates (not in this command):\n'
                + '\n'.join(f'  - {t}' for t in stale)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(templates)} templates processed. ({count_new} new, {count_updated} updated)'
        ))
