"""
Management command to create the default Chart Templates for all chapters.
These templates map to the data models imported from CSV files.
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate

class Command(BaseCommand):
    help = 'Creates/Updates Chart Templates for all supported chapters.'

    def handle(self, *args, **options):
        templates = []

        # ====================================================================
        # LIVESTOCK & FISHERIES (6 templates)
        # ====================================================================
        self.stdout.write('Creating Chart Templates for Livestock & Fisheries...')
        templates.extend([
            {
                'title': 'Number of Livestock',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'LivestockNumbers',
                'x_column': 'year',
                'y_columns': ['hybrid_cows', 'native_cows', 'buffalo'],
                'dataset_config': [
                    {'label': 'Hybrid Cows', 'borderColor': '#1a4570'},
                    {'label': 'Native Cows', 'borderColor': '#ee8939'},
                    {'label': 'Buffalo', 'borderColor': '#2ca02c'}
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'display_order': 1,
            },
            {
                'title': 'Artificial Insemination Performance',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'line',
                'data_source_table': 'ArtificialInsemination',
                'x_column': 'year',
                'y_columns': ['annual_target', 'actual_numbers'],
                'dataset_config': [
                    {'label': 'Annual Target', 'borderColor': '#d62728'},
                    {'label': 'Actual Numbers', 'borderColor': '#9467bd'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 2,
            },
            {
                'title': 'Dairy Cooperatives Overview',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'DairyCooperative',
                'x_column': 'year',
                'y_columns': ['cooperative_societies', 'memberships'],
                'dataset_config': [
                    {'label': 'Cooperative Societies', 'borderColor': '#1a4570'},
                    {'label': 'Memberships', 'borderColor': '#2ca02c'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 3,
            },
            {
                'title': 'Dairy Byproducts',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'DairyByproduct',
                'x_column': 'year',
                'y_columns': ['units'],
                'dataset_config': [
                    {'label': 'Units', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'item',
                'display_order': 4,
            },
            {
                'title': 'Fisheries Production',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'line',
                'data_source_table': 'Fisheries',
                'x_column': 'year',
                'y_columns': ['groundwater_fish_production'],
                'dataset_config': [
                    {'label': 'Fish Production (Tonnes)', 'borderColor': '#17becf'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 5,
            },
            {
                'title': 'Veterinary Facilities',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'stackedBar',
                'data_source_table': 'Veterinary',
                'x_column': 'year',
                'y_columns': ['veterinary_hospitals', 'first_aid_centres', 'other_facilities'],
                'dataset_config': [
                    {'label': 'Hospitals', 'borderColor': '#e377c2'},
                    {'label': 'First Aid Centres', 'borderColor': '#7f7f7f'},
                    {'label': 'Other Facilities', 'borderColor': '#bcbd22'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 6,
            }
        ])

        # ====================================================================
        # AGRICULTURE (14 templates — matching existing static charts)
        # ====================================================================
        self.stdout.write('Creating Chart Templates for Agriculture...')
        templates.extend([
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
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#2ca02c'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#d62728'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#9467bd'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 1,
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
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#2ca02c'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#d62728'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#9467bd'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 2,
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
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#2ca02c'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#d62728'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#9467bd'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 3,
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
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#2ca02c'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#d62728'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#9467bd'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 4,
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
                'display_order': 5,
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
                    {'label': 'Irrigated Area', 'borderColor': '#2ca02c'},
                    {'label': 'Unirrigated Area', 'borderColor': '#d62728'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 6,
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
                    {'label': 'Share Irrigated (%)', 'borderColor': '#17becf'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 7,
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
                    {'label': 'Irrigated Area', 'borderColor': '#2ca02c'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 8,
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
                    {'label': 'Share Irrigated (%)', 'borderColor': '#e377c2'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 9,
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
                    {'label': 'Actually Uncultivated Area', 'borderColor': '#8c564b'},
                    {'label': 'Other Fallow Land', 'borderColor': '#bcbd22'},
                    {'label': 'Cultivable Waste Land', 'borderColor': '#7f7f7f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 10,
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
                    {'label': 'Kharif', 'borderColor': '#2ca02c'},
                    {'label': 'Rabi', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 11,
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
                    {'label': 'Medium', 'borderColor': '#2ca02c'},
                    {'label': 'Big', 'borderColor': '#d62728'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 12,
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
                    {'label': 'Ponds/Village Lakes', 'borderColor': '#17becf'},
                    {'label': 'Storage Dams', 'borderColor': '#9467bd'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 13,
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
                    {'label': 'Hand Pumps', 'borderColor': '#2ca02c'},
                    {'label': 'Electric Pumps', 'borderColor': '#d62728'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 14,
            },
        ])

        # ====================================================================
        # Process all templates
        # ====================================================================
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
