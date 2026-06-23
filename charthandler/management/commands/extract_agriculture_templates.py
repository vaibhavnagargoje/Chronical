"""
Management command to create/update Chart Templates for the Agriculture chapter.
Charts matching http://127.0.0.1:8000/statistics/maharashtra/<district>/agriculture/

Reference mapping: Agriculture/Original Data/agriculture_reference.xlsx
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate


def build_chart_options(
    y_axis_title,
    x_axis_title='Year',
    is_percent=False,
    is_stacked=False,
    disable_all_filter1=False,
    disable_all_filter2=False,
):
    options = {
        'scales': {
            'x': {'title': {'display': True, 'text': x_axis_title}},
            'y': {'beginAtZero': True, 'title': {'display': True, 'text': y_axis_title}},
        }
    }
    if is_stacked:
        options['scales']['x']['stacked'] = True
        options['scales']['y']['stacked'] = True
    if is_percent:
        options['is_percentage_format'] = True
    if disable_all_filter1:
        options['disable_all_filter1'] = True
    if disable_all_filter2:
        options['disable_all_filter2'] = True
    return options


class Command(BaseCommand):
    help = 'Creates/Updates Chart Templates for the Agriculture chapter.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Agriculture...\n')

        templates = [
            # ==================================================================
            # SECTION 1: IRRIGATION
            # ==================================================================
            {
                'title': 'A. No. of Projects',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'DsaIrrigationprojects',
                'x_column': 'year',
                'y_columns': ['small_local', 'small_state', 'medium', 'big'],
                'dataset_config': [
                    {'label': 'Small (Local)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Small (State)', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Medium', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Big', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Projects'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 1,
            },
            {
                'title': 'B. No. of Ponds/Village Lakes and Storage Dams',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'DsaIrrigationfacilities',
                'x_column': 'year',
                'y_columns': ['ponds_or_village_lakes', 'storage_dams'],
                'dataset_config': [
                    {'label': 'Ponds or Village Lakes', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Storage Dams', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 2,
            },
            {
                'title': 'C. Irrigation Beneficiary Area vs Irrigated Area',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'DsaIrrigationbeneficiary',
                'x_column': 'year',
                'y_columns': ['irrigation_beneficiary_area', 'irrigated_area'],
                'dataset_config': [
                    {'label': 'Irrigation Beneficiary Area', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Irrigated Area', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'project_size',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Area (in Hectares)'),
                'description': 'District Statistical Abstracts',
                'additional_info': 'Beneficiary area represents the target area that was planned for coverage, while irrigated area shows the actual area that was irrigated.',
                'display_order': 3,
            },
            {
                'title': 'D. Share of Beneficiary Area Irrigated',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'DsaIrrigationbeneficiary',
                'x_column': 'year',
                'y_columns': ['share_of_beneficiary_area_irrigated'],
                'dataset_config': [
                    {'label': 'Share of Beneficiary Area Irrigated', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'project_size',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Share (%)', is_percent=True),
                'description': 'District Statistical Abstracts',
                'additional_info': 'Beneficiary area represents the target area that was planned for coverage, while irrigated area shows the actual area that was irrigated.',
                'display_order': 4,
            },
            {
                'title': 'E. Tubewells and Pumps Installed In The Year',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'DsaTubewellshandpumps',
                'x_column': 'year',
                'y_columns': ['all_tubewells', 'high_capacity_tubewells', 'successful_tubewells', 'hand_pumps', 'electric_pumps'],
                'dataset_config': [
                    {'label': 'All Tubewells', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'High Capacity Tubewells', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Successful Tubewells', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Hand Pumps', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                    {'label': 'Electric Pumps', 'borderColor': '#7a9e60', 'backgroundColor': '#7a9e60'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 5,
            },
            {
                'title': 'F. Irrigation and Water Pumping Facilities',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'DsaIrrigationwells',
                'x_column': 'year',
                'y_columns': ['total_irrigation_wells', 'wells_in_use_with_diesel_pump', 'wells_in_use_with_electric_pump', 'irrigation_wells_not_in_use'],
                'dataset_config': [
                    {'label': 'Total Irrigation Wells', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Wells In Use With Diesel Pump', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Wells In Use With Electric Pump', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                    {'label': 'Irrigation Wells Not in Use', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 6,
            },
            
            # ==================================================================
            # SECTION 2: CROPPING METRICS
            # ==================================================================
            {
                'title': 'A. Share in Total Holdings',
                'chapter_type': 'agriculture',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'AgcLanduse',
                'x_column': 'year',
                'y_columns': ['area_classified_as_cultivated', 'area_classified_as_uncultivated', 'area_not_available_for_agriculture'],
                'dataset_config': [
                    {'label': 'Area Classified as Cultivated', 'backgroundColor': '#1a4570'},
                    {'label': 'Area Classified as Uncultivated', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Area Not Available For Agriculture', 'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'size_class',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Percentage Share'),
                'description': 'Agriculture Census, Dept of Agriculture & Farmers Welfare',
                'additional_info': 'Note: Data for 2005 is currently unavailable and will be added soon.',
                'display_order': 7,
            },
            {
                'title': 'B. Cultivated Area (With Components)',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'AgcLanduse',
                'x_column': 'year',
                'y_columns': ['net_sown_area', 'current_fallow'],
                'dataset_config': [
                    {'label': 'Net Sown Area', 'backgroundColor': '#1a4570'},
                    {'label': 'Current Fallow', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'size_class',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Area (in Hectares)'),
                'description': 'Agriculture Census, Dept of Agriculture & Farmers Welfare',
                'additional_info': 'Note: Data for 2005 is currently unavailable and will be added soon. Net sown area is land sown at least once in a year. Current fallow land is land left uncultivated for one season but expected to be used again soon.',
                'display_order': 8,
            },
            {
                'title': 'C. Gross Cropped Area (Irrigated + Unirrigated)',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'AgcGrosscroppedarea',
                'x_column': 'year',
                'y_columns': ['irrigated_area', 'unirrigated_area'],
                'dataset_config': [
                    {'label': 'Irrigated Area', 'backgroundColor': '#1a4570'},
                    {'label': 'Unirrigated Area', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'size_class',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Area (in Hectares)'),
                'description': 'Agriculture Census, Dept of Agriculture & Farmers Welfare',
                'additional_info': 'Note: Data for 2005 is currently unavailable and will be added soon.',
                'display_order': 9,
            },
            {
                'title': 'D. Share of Cropped Area Irrigated',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'AgcGrosscroppedarea',
                'x_column': 'year',
                'y_columns': ['share_of_cropped_area_irrigated'],
                'dataset_config': [
                    {'label': 'Share of Cropped Area Irrigated', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'size_class',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Share Irrigated', is_percent=True),
                'description': 'Agriculture Census, Dept of Agriculture & Farmers Welfare',
                'additional_info': 'Note: Data for 2005 is currently unavailable and will be added soon.',
                'display_order': 10,
            },
            {
                'title': 'E. Distribution of Chemical Fertilizers',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'DsaChemicalfertilizer',
                'x_column': 'year',
                'y_columns': ['kharif', 'rabi'],
                'dataset_config': [
                    {'label': 'Kharif', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Rabi', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Amount (in metric tonnes'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 11,
            },

            # ==================================================================
            # SECTION 3: LAND USE AND CREDIT
            # ==================================================================
            {
                'title': 'A. Area of Agricultural Land Holdings (With Size Group)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'AgcHoldingsarea',
                'x_column': 'year',
                'y_columns': ['marginal_below_1_ha', 'small_1_to_2_ha', 'semimedium_2_to_4_ha', 'medium_4_to_10_ha', 'large_10_ha'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'backgroundColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Semimedium (2 to 4 ha)', 'backgroundColor': '#e46e53'},
                    {'label': 'Medium (4 to 10 ha)', 'backgroundColor': '#af7c50'},
                    {'label': 'Large (>10 ha)', 'backgroundColor': '#7a9e60'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Area (in Hectares)'),
                'description': 'Agriculture Census, Dept of Agriculture & Farmers Welfare',
                'additional_info': 'Note: Data for 2005 is currently unavailable and will be added soon.',
                'display_order': 12,
            },
            {
                'title': "B. Size Groups' Share in Total Agricultural Land Area",
                'chapter_type': 'agriculture',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'AgcHoldingsarea',
                'x_column': 'year',
                'y_columns': ['marginal_below_1_ha', 'small_1_to_2_ha', 'semimedium_2_to_4_ha', 'medium_4_to_10_ha', 'large_10_ha'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'backgroundColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Semimedium (2 to 4 ha)', 'backgroundColor': '#e46e53'},
                    {'label': 'Medium (4 to 10 ha)', 'backgroundColor': '#af7c50'},
                    {'label': 'Large (>10 ha)', 'backgroundColor': '#7a9e60'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Share in Total'),
                'description': 'Agriculture Census, Dept of Agriculture & Farmers Welfare',
                'additional_info': 'Note: Data for 2005 is currently unavailable and will be added soon.',
                'display_order': 13,
            },
            {
                'title': 'C. No. of Agricultural Land Holdings (With Size Group)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'AgcHoldingsnumber',
                'x_column': 'year',
                'y_columns': ['marginal_below_1_ha', 'small_1_to_2_ha', 'semimedium_2_to_4_ha', 'medium_4_to_10_ha', 'large_10_ha'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'backgroundColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Semimedium (2 to 4 ha)', 'backgroundColor': '#e46e53'},
                    {'label': 'Medium (4 to 10 ha)', 'backgroundColor': '#af7c50'},
                    {'label': 'Large (>10 ha)', 'backgroundColor': '#7a9e60'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Number. of Land Holdings'),
                'description': 'Agriculture Census, Dept of Agriculture & Farmers Welfare',
                'additional_info': 'Note: Data for 2005 is currently unavailable and will be added soon.',
                'display_order': 14,
            },
            {
                'title': "D. Size Group's Share in Total No. of Agricultural Land Holdings",
                'chapter_type': 'agriculture',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'AgcHoldingsnumber',
                'x_column': 'year',
                'y_columns': ['marginal_below_1_ha', 'small_1_to_2_ha', 'semimedium_2_to_4_ha', 'medium_4_to_10_ha', 'large_10_ha'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'backgroundColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Semimedium (2 to 4 ha)', 'backgroundColor': '#e46e53'},
                    {'label': 'Medium (4 to 10 ha)', 'backgroundColor': '#af7c50'},
                    {'label': 'Large (>10 ha)', 'backgroundColor': '#7a9e60'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Share of Total Holdings'),
                'description': 'Agriculture Census, Dept of Agriculture & Farmers Welfare',
                'additional_info': 'Note: Data for 2005 is currently unavailable and will be added soon.',
                'display_order': 15,
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
        # Warn about any stale agriculture templates not in this list
        # ------------------------------------------------------------------
        expected_titles = {config['title'] for config in templates}
        stale = list(
            ChartTemplate.objects
            .filter(chapter_type='agriculture')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale:
            self.stdout.write(self.style.WARNING(
                '\nStale agriculture templates (not in this command):\n'
                + '\n'.join(f'  - {t}' for t in stale)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(templates)} templates processed. ({count_new} new, {count_updated} updated)'
        ))
