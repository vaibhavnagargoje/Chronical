"""
Management command to create the default Chart Templates for Agriculture.
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate

class Command(BaseCommand):
    help = 'Creates/Updates Chart Templates for Agriculture.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Agriculture...')
        templates = [
            # 1. Area of Agricultural Land Holdings (With Size Group)
            {
                'title': 'Area of Agricultural Land Holdings (With Size Group)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'HoldingsArea',
                'x_column': 'year',
                'y_columns': ['marginal', 'small', 'semimedium', 'medium', 'large'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'borderColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'borderColor': '#ee8939'},
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#f5b843'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#8b3834'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#e0ba3f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 18,
            },
            # 2. Size Groups' Share in Total Agricultural Land Holdings Area
            {
                'title': "Size Groups' Share in Total Agricultural Land Holdings Area",
                'chapter_type': 'agriculture',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'HoldingsArea',
                'x_column': 'year',
                'y_columns': ['marginal', 'small', 'semimedium', 'medium', 'large'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'borderColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'borderColor': '#ee8939'},
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#f5b843'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#8b3834'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#e0ba3f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 19,
            },
            # 3. No. of Agricultural Land Holdings (With Size Group)
            {
                'title': 'No. of Agricultural Land Holdings (With Size Group)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'HoldingsNumber',
                'x_column': 'year',
                'y_columns': ['marginal', 'small', 'semimedium', 'medium', 'large'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'borderColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'borderColor': '#ee8939'},
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#f5b843'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#8b3834'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#e0ba3f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 20,
            },
            # 4. Size Groups' Share in Total No. of Agricultural Land Holdings
            {
                'title': "Size Groups' Share in Total No. of Agricultural Land Holdings",
                'chapter_type': 'agriculture',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'HoldingsNumber',
                'x_column': 'year',
                'y_columns': ['marginal', 'small', 'semimedium', 'medium', 'large'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'borderColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'borderColor': '#ee8939'},
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#f5b843'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#8b3834'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#e0ba3f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 21,
            },
            # 5. Cultivated Area (With Components) — from LandUse
            {
                'title': 'Cultivated Area (With Components)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'LandUse',
                'x_column': 'year',
                'y_columns': ['net_sown_area', 'current_fallow'],
                'dataset_config': [
                    {'label': 'Net Area Sown', 'borderColor': '#1a4570'},
                    {'label': 'Current Fallow', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 22,
            },
            # 6. Gross Cropped Area (Irrigated + Unirrigated)
            {
                'title': 'Gross Cropped Area (Irrigated + Unirrigated)',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'GrossCroppedArea',
                'x_column': 'year',
                'y_columns': ['irrigated_area', 'unirrigated_area'],
                'dataset_config': [
                    {'label': 'Irrigated Area', 'borderColor': '#1a4570'},
                    {'label': 'Unirrigated Area', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 23,
            },
            # 7. Share of Cropped Area Irrigated
            {
                'title': 'Share of Cropped Area Irrigated',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'GrossCroppedArea',
                'x_column': 'year',
                'y_columns': ['share_cropped_area_irrigated'],
                'dataset_config': [
                    {'label': 'Share Irrigated (%)', 'borderColor': '#f5b843'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 24,
            },
            # 8. Irrigation Beneficiary Area vs Irrigated Area
            {
                'title': 'Irrigation Beneficiary Area vs Irrigated Area',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'IrrigationBeneficiary',
                'x_column': 'year',
                'y_columns': ['irrigation_beneficiary_area', 'irrigated_area'],
                'dataset_config': [
                    {'label': 'Beneficiary Area', 'borderColor': '#1a4570'},
                    {'label': 'Irrigated Area', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 25,
            },
            # 9. Share of Beneficiary Area Irrigated
            {
                'title': 'Share of Beneficiary Area Irrigated',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'IrrigationBeneficiary',
                'x_column': 'year',
                'y_columns': ['share_beneficiary_area_irrigated'],
                'dataset_config': [
                    {'label': 'Share Irrigated (%)', 'borderColor': '#f5b843'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 26,
            },
            # 10. Uncultivated Area (With Components) — from LandUse
            {
                'title': 'Uncultivated Area (With Components)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'LandUse',
                'x_column': 'year',
                'y_columns': ['actually_uncultivated_area', 'other_fallow_land', 'cultivable_waste_land'],
                'dataset_config': [
                    {'label': 'Actually Uncultivated Area', 'borderColor': '#1a4570'},
                    {'label': 'Other Fallow Land', 'borderColor': '#ee8939'},
                    {'label': 'Cultivable Waste Land', 'borderColor': '#f5b843'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 27,
            },
            # 11. Distribution of Chemical Fertilizers
            {
                'title': 'Distribution of Chemical Fertilizers',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'ChemicalFertilizer',
                'x_column': 'year',
                'y_columns': ['kharif', 'rabi'],
                'dataset_config': [
                    {'label': 'Kharif', 'borderColor': '#1a4570'},
                    {'label': 'Rabi', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 28,
            },
            # 12. No. of Irrigation Projects
            {
                'title': 'No. of Irrigation Projects',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'IrrigationProjects',
                'x_column': 'year',
                'y_columns': ['small_local', 'small_state', 'medium', 'big'],
                'dataset_config': [
                    {'label': 'Small (Local)', 'borderColor': '#1a4570'},
                    {'label': 'Small (State)', 'borderColor': '#ee8939'},
                    {'label': 'Medium', 'borderColor': '#f5b843'},
                    {'label': 'Big', 'borderColor': '#8b3834'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 29,
            },
            # 13. No. of Ponds/Village Lakes and Storage Dams
            {
                'title': 'No. of Ponds/Village Lakes and Storage Dams',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'IrrigationFacilities',
                'x_column': 'year',
                'y_columns': ['ponds_village_lakes', 'storage_dams'],
                'dataset_config': [
                    {'label': 'Ponds/Village Lakes', 'borderColor': '#1a4570'},
                    {'label': 'Storage Dams', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 30,
            },
            # 14. Tubewells and Pumps
            {
                'title': 'Tubewells and Pumps Installed In The Year',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'TubewellsHandpumps',
                'x_column': 'year',
                'y_columns': ['all_tubewells', 'high_capacity_tubewells', 'hand_pumps', 'electric_pumps'],
                'dataset_config': [
                    {'label': 'All Tubewells', 'borderColor': '#1a4570'},
                    {'label': 'High Capacity Tubewells', 'borderColor': '#ee8939'},
                    {'label': 'Hand Pumps', 'borderColor': '#f5b843'},
                    {'label': 'Electric Pumps', 'borderColor': '#8b3834'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 31,
            },
        ]

        count = 0
        for config in templates:
            obj, created = ChartTemplate.objects.update_or_create(
                title=config['title'],
                chapter_type=config['chapter_type'],
                defaults=config
            )
            if created:
                count += 1
                self.stdout.write(f"  [NEW] {obj.title}")
            else:
                self.stdout.write(f"  [UPD] {obj.title}")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Processed {len(templates)} templates. ({count} new)'
        ))
